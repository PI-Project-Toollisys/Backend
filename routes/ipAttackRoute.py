from bson.objectid import ObjectId
from fastapi import APIRouter
from conf.db import client
from bson import ObjectId

from models.ipAttackModel import IpAttack
from schemas.ipAttackSchema import ipAttackEntity, ipAttacksEntity

ipAttackAPI = APIRouter()


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
async def postIpAttack(ipAttack: IpAttack):
    try:
        client.maindb.ipattack.insert_one(dict(ipAttack))
        return ipAttacksEntity(client.maindb.ipattack.find())
    except:
        return dict([])


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
