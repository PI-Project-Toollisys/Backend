from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException
from pymongo import SLOW_ONLY
from conf.db import client
from bson import ObjectId

from models.ipAttackModel import IpAttack, postAttack
from schemas.ipAttackSchema import ipAttackEntity, ipAttacksEntity

import socket, argparse, os, json
from multiprocessing import Process, Manager
from time import sleep
from attack.mainAttack import attack

ipAttackAPI = APIRouter(tags=['Ip Attack'])


@ipAttackAPI.get('/getAllIpAttacks')
# Get all ipAttack to database
async def getAllIpAttacks():
    return ipAttacksEntity(client.maindb.ipattack.find())


@ipAttackAPI.get('/getOneIpAttack/{id}')
# Get a ipAttack to database by id
async def getOneIpAttack(id):
    try:
        return ipAttackEntity(client.maindb.ipattack.find_one({"_id": ObjectId(id)}))
    except:
        return dict([])


@ipAttackAPI.get('/getIpAttacks/{value}')
# Get all ipAttack to database by value (cnpj or date)
async def getIpAttacksBy(value):
    if value.isnumeric():
        return ipAttacksEntity(client.maindb.ipattack.find({"firm": value}))
    else:
        return ipAttacksEntity(client.maindb.ipattack.find({"date": value}))


@ipAttackAPI.post('/postIpAttack')
# Post ipAttack without process to database
async def postIpAttack(ipAttack: postAttack):
    if not client.maindb.firm.find_one({"cnpj": ipAttack.firm}):
        raise HTTPException(status_code=404, detail="Invalid Firm")

    if client.maindb.ipattack.find_one({"firm": ipAttack.firm,"date":ipAttack.date}):
        raise HTTPException(status_code=404, detail="Already Exist")

    jsonReturn ={
        "firm":ipAttack.firm,
        "date":ipAttack.date,
        "listIp":ipAttack.listIp,
        "port":ipAttack.port,
        "numReq":ipAttack.numReq,
        "numProcess":ipAttack.numProcess,
        "process":[]
    }

    try:
        _id = client.maindb.ipattack.insert_one(jsonReturn)
        return ipAttackEntity(client.maindb.ipattack.find_one({"_id": ObjectId(_id.inserted_id)}))
    except:
        raise HTTPException(status_code=404, detail="Invalid Insert")


@ipAttackAPI.put('/updateIpAttack/{firm}/{date}')
# Update specific ipAttack json filtered by cnpj and date with attack execution
async def updateIpAttack(firm,date):
    if not client.maindb.firm.find_one({"cnpj": firm}):
        raise HTTPException(status_code=404, detail="Invalid Firm")
    
    ipAttackGet = client.maindb.ipattack.find_one({"firm":firm,"date":date})

    if not ipAttackGet:
        raise HTTPException(status_code=404, detail="Don't Exist the Attack")

    # print('---- Começando o ataque ----')
    # print('Atacando ip: %s porta: %d' %(ipAttackGet["listIp"],ipAttackGet["port"]))
    # print('---- Criando %d processos ----' %ipAttackGet["numProcess"])

    if not ipAttackGet["process"]:
        manager = Manager()
        return_list = manager.list()
        jobs = []

        for ip in ipAttackGet["listIp"]:
            for i in range(ipAttackGet["numProcess"]):
                atck = Process(target=attack, args=(ip, ipAttackGet["port"], ipAttackGet["numReq"],return_list))
                jobs.append(atck)
                atck.start()
        
        for proc in jobs:
            proc.join()

        ipAttackGet["process"] = sorted(return_list, key=lambda d: d["id"])

        try:
            client.maindb.ipattack.find_one_and_update(
                {"firm":firm,"date":date}, {"$set": ipAttackGet})
            return ipAttackEntity(client.maindb.ipattack.find_one({"firm":firm,"date":date}))
        except:
            raise HTTPException(status_code=404, detail="Don't Accept")
    else:
        raise HTTPException(status_code=404, detail="Already Update")


@ipAttackAPI.delete('/delIpAttack/{id}')
# Delete a ipAttack by ID
async def deleteIpAttack(id):
    try:
        return ipAttackEntity(client.maindb.ipattack.find_one_and_delete({"_id": ObjectId(id)}))
    except:
        dict([])
