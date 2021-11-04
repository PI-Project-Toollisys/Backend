from bson.objectid import ObjectId
from fastapi import APIRouter
from conf.db import client
from bson import ObjectId

from models.answerModel import Answer
from schemas.answerSchema import answerEntity, answersEntity

answerAPI = APIRouter()


@answerAPI.get('/getAllAnswers')
# Get all answer to database
async def getAllAnswers():
    try:
        return answersEntity(client.maindb.answer.find())
    except:
        return dict([])


@answerAPI.get('/getOneAnswer/{id}')
# Get all answer to database by id
async def getAnswersById(id):
    try:
        return answerEntity(client.maindb.answer.find_one({"_id": ObjectId(id)}))
    except:
        return dict([])


@answerAPI.get('/getAnswers/{value}')
# Get all answer to database by value (cnpj or date)
async def getAnswers(value):
    if value.isnumeric():
        return answersEntity(client.maindb.answer.find({"firm": str(value)}))
    else:
        return answersEntity(client.maindb.answer.find({"date": str(value)}))


@answerAPI.post('/postAnswer')
# Post answer to database
async def postAnswer(answer: Answer):
    client.maindb.answer.insert_one(dict(answer))
    return answersEntity(client.maindb.answer.find())


@answerAPI.put('/updateAnswer/{id}')
# Upate a answer by ID
async def updateAnswer(id, answer: Answer):
    try:
        client.maindb.answer.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": dict(answer)})
        return answerEntity(client.maindb.answer.find_one({"_id": ObjectId(id)}))
    except:
        return dict([])


@answerAPI.delete('/delAnswer/{id}')
# Delete a answer by ID
async def deleteAnswer(id):
    try:
        return answerEntity(client.maindb.answer.find_one_and_delete({"_id": ObjectId(id)}))
    except:
        dict([])
