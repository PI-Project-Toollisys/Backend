from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from authentication.oaut2 import get_current_user
from conf.db import client
from bson import ObjectId
import numpy as np

from models.answerModel import Answer
from schemas.answerSchema import answerEntity, answersEntity

answerAPI = APIRouter(tags=['Answer'])

questionsList = ["rec","arm","ent","exp","ins","com","aca","inft","infm","dad",]

@answerAPI.get('/getAllAnswers')
# Get all answer to database
async def getAllAnswers():
    return answersEntity(client.maindb.answer.find())


@answerAPI.get('/getAnswers/{value}')
# Get all answer to database by value (cnpj or date)
async def getAnswers(value):
    if value.isnumeric():
        if not client.maindb.firm.find_one({"cnpj": value}):
            raise HTTPException(status_code=404, detail="Firm not found")
        return answersEntity(client.maindb.answer.find({"firm": str(value)}))
    else:
        resultByDate = answersEntity(client.maindb.answer.find({"date": str(value)}))
        if not resultByDate:
            raise HTTPException(status_code=404, detail="Answers by date not found")
        else:
            return resultByDate


@answerAPI.get('/getScoreFirmByQuestion/{firm}/{quest}')
# Get all answers in especific question
async def getScoreAnswersByQuestion(firm,quest):
    if not client.maindb.firm.find_one({"cnpj": firm}):
        raise HTTPException(status_code=404, detail="Firm not found")

    n=client.maindb.answer.find({"firm": str(firm)}).count()

    if quest not in questionsList:
        raise HTTPException(status_code=404, detail="Quest not found")
    if quest == "rec" or quest == "ent":
        sumResult = list(np.zeros(5))
    elif quest == "inft":
        sumResult = list(np.zeros(4))
    else:
        sumResult = list(np.zeros(3))
    for doc in client.maindb.answer.find({"firm": str(firm)},{quest:1}):
        sumResult = [ (a + b) for a, b in zip(sumResult, doc[quest]['answers']) ]

    sumResult = list(map(lambda x: x/n, sumResult))

    return sumResult


@answerAPI.get('/getScoreFirmTotal/{firm}')
# pergar todas as respostas, somar o valor e partir da quantidade
# que possui (relacionados a firma) dividir e obter a média
# da pontuação
async def getScoreTotal(firm):
    if not client.maindb.firm.find_one({"cnpj": firm}):
        raise HTTPException(status_code=404, detail="Firm not found")

    answers = answersEntity(client.maindb.answer.find({"firm": str(firm)}))

    if not answers:
        raise HTTPException(status_code=404, detail="Doesn't has answers")

    n = client.maindb.answer.find({"firm": str(firm)}).count()
    
    dictAux = {
        "firm": str(firm),
        "rec":{
            "title": "Reconhecimento",
            "answers":[0,0,0,0,0]
        },
        "arm":{
            "title": "Armamento",
            "answers":[0,0,0]
        },
        "ent":{
            "title": "Entrega",
            "answers":[0,0,0,0,0]
        },
        "exp":{
            "title": "Exploracao",
            "answers":[0,0,0]
        },
        "ins":{
            "title": "Instalacao",
            "answers":[0,0,0]
        },
        "com":{
            "title": "ComandoControle",
            "answers":[0,0,0]
        },
        "aca":{
            "title": "AcaoObjetivo",
            "answers":[0,0,0]
        },
        "inft":{
            "title": "Infraestrutura",
            "answers":[0,0,0,0]
        },
        "infm":{
            "title": "informacao",
            "answers":[0,0,0]
        },
        "dad":{
            "title": "Dados",
            "answers":[0,0,0]   
        }
    }
    
    for doc in answers:
        for item in doc:
            if item == "id" or item == "firm" or item == "date":
                pass
            else:
                dictAux[item]['answers'] = [ (a + b) for a, b in zip(dictAux[item]['answers'], doc[item]['answers']) ]
            
    for item in dictAux:
        if item != "firm":
            dictAux[item]['answers'] = list(map(lambda x: x/n, dictAux[item]['answers']))

    return dictAux

@answerAPI.get('/getScoreByQuestionSum/{firm}')
# pergar a questão específica de todas as respostas
# para somar e dividir pela quantidade dela (média)
async def getScoreByQuestionSum(firm):
    dictAux = {
    "firm": firm,
    "score_total": 0
    }

    if not client.maindb.firm.find_one({"cnpj": firm}):
        raise HTTPException(status_code=404, detail="Firm not found")
    
    answers = answersEntity(client.maindb.answer.find({"firm": str(firm)}))

    if not answers:
        raise HTTPException(status_code=200, detail="Doesn't has answers")
    
    n = client.maindb.answer.find({"firm": str(firm)}).count()
    
    for doc in answers:
        for item in doc:
            if item == "id" or item == "firm" or item == "date":
                pass
            else:
                dictAux["score_total"] += sum(doc[item]['answers'])

    dictAux["score_total"] = float(dictAux["score_total"]/n)
    return dictAux


@answerAPI.post('/postAnswer')
# Post answer to database
async def postAnswer(answer: Answer):
    _id = client.maindb.answer.insert_one(dict(answer))
    print(_id.inserted_id)
    return answerEntity(client.maindb.answer.find_one({"_id": ObjectId(str(_id.inserted_id))}))


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
        raise HTTPException(status_code=404, detail="Doesn't has answer")
