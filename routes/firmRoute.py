from warnings import resetwarnings
from bson.objectid import ObjectId
from fastapi import APIRouter
from pymongo.common import validate_type_registry
from conf.db import client
from bson import ObjectId

from models.firmModel import Firm
from schemas.firmSchema import firmEntity, firmsEntity

firmAPI = APIRouter()


@firmAPI.get('/getAllFirms')
# Get all firm to database
async def getAllFirms():
    try:
        return firmsEntity(client.maindb.firm.find())
    except:
        return dict([])


@firmAPI.get('/getOneFirm/{value}')
# Get one firm to database by value
async def getOneFirm(value):
    try:
        valueAux = str(value).replace(' ', '')
        valueAux = valueAux.replace('.', '')
        valueAux = valueAux.replace(',', '')

        if valueAux.isnumeric():  # CNPJ
            return firmEntity(client.maindb.firm.find_one({"cnpj": str(value)}))
        elif valueAux.isalpha():  # Name
            return firmEntity(client.maindb.firm.find_one({"name": str(value)}))
        else:  # Name or ID
            # ID
            # print(bool(client.maindb.firm.find({"_id": ObjectId(value)}).count()))
            veriID = bool(client.maindb.firm.find(
                {"_id": ObjectId(value)}).count())
            veriName = bool(client.maindb.firm.find(
                {"name": str(value)}).count())
            if veriID:
                print(str(value))
                return firmEntity(client.maindb.firm.find_one({"_id": ObjectId(value)}))
            elif veriName:  # Name
                return firmEntity(client.maindb.firm.find_one({"name": str(value)}))
    except:
        return dict([])


@ firmAPI.post('/postFirm')
# Post firm to database
async def postFirm(firm: Firm):
    client.maindb.firm.insert_one(dict(firm))
    return firmsEntity(client.maindb.firm.find())


@ firmAPI.put('/updateFirm/{id}')
# Update a firma by ID
async def updateFirm(id, firm: Firm):
    try:
        client.maindb.firm.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": dict(firm)})
        return firmEntity(client.maindb.firm.find_one({"_id": ObjectId(id)}))
    except:
        return dict([])


@ firmAPI.delete('/delFirm/{id}')
# Delete a firm by ID
async def deleteFirm(id):
    try:
        return firmsEntity(client.maindb.firm.find_one_and_delete({"_id": ObjectId(id)}))
    except:
        return dict([])
