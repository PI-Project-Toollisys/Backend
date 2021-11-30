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
# Post ipAttack to database
async def postIpAttack(ipAttack: postAttack):
    if not client.maindb.firm.find_one({"cnpj": ipAttack.firm}):
        raise HTTPException(status_code=404, detail="Invalid Firm")

    print('---- Começando o ataque ----')
    print('Atacando ip: %s porta: %d' %(ipAttack.listIp,ipAttack.port))
    print('---- Criando %d processos ----' %ipAttack.numProcess)

    manager = Manager()
    return_dict = manager.list()
    jobs = []

    for ip in ipAttack.listIp:
        for i in range(ipAttack.numProcess):
            atck = Process(target=attack, args=(ip, ipAttack.port, ipAttack.numReq,return_dict))
            jobs.append(atck)
            atck.start()
    
    for proc in jobs:
        proc.join()
    # print(return_dict)

    jsonReturn ={
        "firm":ipAttack.firm,
        "date":ipAttack.date,
        "process":sorted(return_dict, key=lambda d: d["id"]) 
    }

    try:
        _id = client.maindb.ipattack.insert_one(jsonReturn)
        return ipAttackEntity(client.maindb.ipattack.find_one({"_id": ObjectId(_id.inserted_id)}))
    except:
        raise HTTPException(status_code=404, detail="Invalid Insert")


@ipAttackAPI.put('/updateIpAttack/{id}')
# Upate a ipAttack by ID
async def updateIpAttack(id, ipAttack: IpAttack):
    try:
        client.maindb.ipattack.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": dict(ipAttack)})
        return ipAttackEntity(client.maindb.ipattack.find_one({"_id": ObjectId(id)}))
    except:
        return dict([])


@ipAttackAPI.delete('/delIpAttack/{id}')
# Delete a ipAttack by ID
async def deleteIpAttack(id):
    try:
        return ipAttackEntity(client.maindb.ipattack.find_one_and_delete({"_id": ObjectId(id)}))
    except:
        dict([])
