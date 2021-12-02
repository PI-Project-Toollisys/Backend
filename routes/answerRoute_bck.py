from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from authentication.oaut2 import get_current_user
from conf.db import client
from bson import ObjectId

from models.answerModel import Answer
from schemas.answerSchema import answerEntity, answersEntity
from models.userModel import User

answerAPI = APIRouter(tags=['Answer'])


@answerAPI.get('/getAllAnswers')
# Get all answer to database
async def getAllAnswers(current_user: User = Depends(get_current_user)):
    try:
        return answersEntity(client.maindb.answer.find())
    except:
        return dict([])


# @answerAPI.get('/getOneAnswer/{id}')
# # Get all answer to database by id
# async def getAnswersById(id):
#     try:
#         return answerEntity(client.maindb.answer.find_one({"_id": ObjectId(id)}))
#     except:
#         return dict([])


@answerAPI.get('/getAnswers/{value}')
# Get all answer to database by value (cnpj or date)
async def getAnswers(value):
    if value.isnumeric():
        return answersEntity(client.maindb.answer.find({"firm": str(value)}))
    else:
        return answersEntity(client.maindb.answer.find({"date": str(value)}))


@answerAPI.get('/getScoreFirmByQuestion/{firm}/{quest}')
# Get all answers in especific question
async def getScoreAnswersByQuestion(firm,quest):
    try:
        sumResult = 0
        for doc in client.maindb.answer.find({"firm": str(firm)},{quest:1}):
            sumResult += doc[quest][1]
        sumResult = float(sumResult/client.maindb.answer.find({"firm": str(firm)}).count())
        return {'firm':firm,quest:float(sumResult)}
    except:
        return dict([])


@answerAPI.get('/getScoreFirmTotal/{firm}')
# pergar todas as respostas, somar o valor e partir da quantidade
# que possui (relacionados a firma) dividir e obter a média
# da pontuação
async def getScoreTotal(firm):
    dictAux = {
    "firm": firm,
    "rec1": 0,
    "rec2": 0,
    "rec3": 0,
    "rec4": 0,
    "rec5": 0,
    "arm1": 0,
    "arm2": 0,
    "arm3": 0,
    "ent1": 0,
    "ent2": 0,
    "ent3": 0,
    "ent4": 0,
    "ent5": 0,
    "exp1": 0,
    "exp2": 0,
    "exp3": 0,
    "ins1": 0,
    "ins2": 0,
    "ins3": 0,
    "com1": 0,
    "com2": 0,
    "com3": 0,
    "aca1": 0,
    "aca2": 0,
    "aca3": 0,
    "inf1": 0,
    "inf2": 0,
    "inf3": 0,
    "inf4": 0,
    "int1": 0,
    "int2": 0,
    "int3": 0,
    "dad1": 0,
    "dad2": 0,
    "dad3": 0
    }

    answers = answersEntity(client.maindb.answer.find({"firm": str(firm)}))
    
    if not answers:
        raise HTTPException(status_code=404, detail="Invalid Login")

    for doc in answers:
        dictAux["rec1"] += int(doc["rec1"][1])
        dictAux["rec2"] += int(doc["rec2"][1])
        dictAux["rec3"] += int(doc["rec3"][1])
        dictAux["rec4"] += int(doc["rec4"][1])
        dictAux["rec5"] += int(doc["rec5"][1])
        dictAux["arm1"] += int(doc["arm1"][1])
        dictAux["arm2"] += int(doc["arm2"][1])
        dictAux["arm3"] += int(doc["arm3"][1])
        dictAux["ent1"] += int(doc["ent1"][1])
        dictAux["ent2"] += int(doc["ent2"][1])
        dictAux["ent3"] += int(doc["ent3"][1])
        dictAux["ent4"] += int(doc["ent4"][1])
        dictAux["ent5"] += int(doc["ent5"][1])
        dictAux["exp1"] += int(doc["exp1"][1])
        dictAux["exp2"] += int(doc["exp2"][1])
        dictAux["exp3"] += int(doc["exp3"][1])
        dictAux["ins1"] += int(doc["ins1"][1])
        dictAux["ins2"] += int(doc["ins2"][1])
        dictAux["ins3"] += int(doc["ins3"][1])
        dictAux["com1"] += int(doc["com1"][1])
        dictAux["com2"] += int(doc["com2"][1])
        dictAux["com3"] += int(doc["com3"][1])
        dictAux["aca1"] += int(doc["aca1"][1])
        dictAux["aca2"] += int(doc["aca2"][1])
        dictAux["aca3"] += int(doc["aca3"][1])
        dictAux["inf1"] += int(doc["inf1"][1])
        dictAux["inf2"] += int(doc["inf2"][1])
        dictAux["inf3"] += int(doc["inf3"][1])
        dictAux["inf4"] += int(doc["inf4"][1])
        dictAux["int1"] += int(doc["int1"][1])
        dictAux["int2"] += int(doc["int2"][1])
        dictAux["int3"] += int(doc["int3"][1])
        dictAux["dad1"] += int(doc["dad1"][1])
        dictAux["dad2"] += int(doc["dad2"][1])
        dictAux["dad3"] += int(doc["dad3"][1])
    
    n = client.maindb.answer.find({"firm": str(firm)}).count()

    dictAux["rec1"] = float(dictAux["rec1"]/n)
    dictAux["rec2"] = float(dictAux["rec2"]/n)
    dictAux["rec3"] = float(dictAux["rec3"]/n)
    dictAux["rec4"] = float(dictAux["rec4"]/n)
    dictAux["rec5"] = float(dictAux["rec5"]/n)
    dictAux["arm1"] = float(dictAux["arm1"]/n)
    dictAux["arm2"] = float(dictAux["arm2"]/n)
    dictAux["arm3"] = float(dictAux["arm3"]/n)
    dictAux["ent1"] = float(dictAux["ent1"]/n)
    dictAux["ent2"] = float(dictAux["ent2"]/n)
    dictAux["ent3"] = float(dictAux["ent3"]/n)
    dictAux["ent4"] = float(dictAux["ent4"]/n)
    dictAux["ent5"] = float(dictAux["ent5"]/n)
    dictAux["exp1"] = float(dictAux["exp1"]/n)
    dictAux["exp2"] = float(dictAux["exp2"]/n)
    dictAux["exp3"] = float(dictAux["exp3"]/n)
    dictAux["ins1"] = float(dictAux["ins1"]/n)
    dictAux["ins2"] = float(dictAux["ins2"]/n)
    dictAux["ins3"] = float(dictAux["ins3"]/n)
    dictAux["com1"] = float(dictAux["com1"]/n)
    dictAux["com2"] = float(dictAux["com2"]/n)
    dictAux["com3"] = float(dictAux["com3"]/n)
    dictAux["aca1"] = float(dictAux["aca1"]/n)
    dictAux["aca2"] = float(dictAux["aca2"]/n)
    dictAux["aca3"] = float(dictAux["aca3"]/n)
    dictAux["inf1"] = float(dictAux["inf1"]/n)
    dictAux["inf2"] = float(dictAux["inf2"]/n)
    dictAux["inf3"] = float(dictAux["inf3"]/n)
    dictAux["inf4"] = float(dictAux["inf4"]/n)
    dictAux["int1"] = float(dictAux["int1"]/n)
    dictAux["int2"] = float(dictAux["int2"]/n)
    dictAux["int3"] = float(dictAux["int3"]/n)
    dictAux["dad1"] = float(dictAux["dad1"]/n)
    dictAux["dad2"] = float(dictAux["dad2"]/n)
    dictAux["dad3"] = float(dictAux["dad3"]/n)
    return dictAux

@answerAPI.get('/getScoreByQuestionSum/{firm}')
# pergar a questão específica de todas as respostas
# para somar e dividir pela quantidade dela (média)
async def getScoreByQuestionSum(firm):
    dictAux = {
    "firm": firm,
    "score_total": 0
    }
    answers = answersEntity(client.maindb.answer.find({"firm": str(firm)}))
    
    if not answers:
        raise HTTPException(status_code=404, detail="Invalid Login")
    for doc in answers:
        dictAux["score_total"] += int(doc["rec1"][1])
        dictAux["score_total"] += int(doc["rec2"][1])
        dictAux["score_total"] += int(doc["rec3"][1])
        dictAux["score_total"] += int(doc["rec4"][1])
        dictAux["score_total"] += int(doc["rec5"][1])
        dictAux["score_total"] += int(doc["arm1"][1])
        dictAux["score_total"] += int(doc["arm2"][1])
        dictAux["score_total"] += int(doc["arm3"][1])
        dictAux["score_total"] += int(doc["ent1"][1])
        dictAux["score_total"] += int(doc["ent2"][1])
        dictAux["score_total"] += int(doc["ent3"][1])
        dictAux["score_total"] += int(doc["ent4"][1])
        dictAux["score_total"] += int(doc["ent5"][1])
        dictAux["score_total"] += int(doc["exp1"][1])
        dictAux["score_total"] += int(doc["exp2"][1])
        dictAux["score_total"] += int(doc["exp3"][1])
        dictAux["score_total"] += int(doc["ins1"][1])
        dictAux["score_total"] += int(doc["ins2"][1])
        dictAux["score_total"] += int(doc["ins3"][1])
        dictAux["score_total"] += int(doc["com1"][1])
        dictAux["score_total"] += int(doc["com2"][1])
        dictAux["score_total"] += int(doc["com3"][1])
        dictAux["score_total"] += int(doc["aca1"][1])
        dictAux["score_total"] += int(doc["aca2"][1])
        dictAux["score_total"] += int(doc["aca3"][1])
        dictAux["score_total"] += int(doc["inf1"][1])
        dictAux["score_total"] += int(doc["inf2"][1])
        dictAux["score_total"] += int(doc["inf3"][1])
        dictAux["score_total"] += int(doc["inf4"][1])
        dictAux["score_total"] += int(doc["int1"][1])
        dictAux["score_total"] += int(doc["int2"][1])
        dictAux["score_total"] += int(doc["int3"][1])
        dictAux["score_total"] += int(doc["dad1"][1])
        dictAux["score_total"] += int(doc["dad2"][1])
        dictAux["score_total"] += int(doc["dad3"][1])
    
    n = (client.maindb.answer.find({"firm": str(firm)}).count())

    dictAux["score_total"] = float(dictAux["score_total"]/n)
    return dictAux


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
