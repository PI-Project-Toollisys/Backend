from bson.objectid import ObjectId
from fastapi import APIRouter
# from passlib.utils.decor import deprecated_method
from conf.db import client
from bson import ObjectId
from passlib.context import CryptContext

from models.userModel import User
from schemas.userSchema import userEntity, usersEntity

userAPI = APIRouter(tags=['User'])


@userAPI.get('/getAllUsers')
# Get all user to database
async def getAllUsers():
    try:
        return usersEntity(client.maindb.user.find())
    except:
        return dict([])


@userAPI.get('/getOneUser/{id}')
# Get all user to database by ID
async def getUsersById(id):
    try:
        return userEntity(client.maindb.user.find_one({"_id": ObjectId(id)}))
    except:
        return dict([])


@userAPI.get('/getUsersByPermission/{permission}')
# Get all user to database by permission
async def getUsersById(permission):
    return usersEntity(client.maindb.user.find({"permission": int(permission)}))


@userAPI.get('/getUsersByFirm/{firm}')
# Get all user to database by firm
async def getUsersById(firm):
    return usersEntity(client.maindb.user.find({"firm": firm}))


@userAPI.get('/getUsersByRI/{register_identifier}')
# Get all user to database by register_identifier (cpf or cnpj)
async def getUsersById(register_identifier):
    return usersEntity(client.maindb.user.find({"register_identifier": int(register_identifier)}))


pwd_cxt =CryptContext(schemes=["bcrypt"],deprecated="auto")
@userAPI.post('/postUser')
# Post user to database
async def postUser(user: User):
    user.password = pwd_cxt.hash(user.password)
    existing_login = client.maindb.user.find_one({"login": user.login})
    existing_ri = client.maindb.user.find_one(
        {"register_identifier": user.register_identifier})

    if not existing_ri:
        if not existing_login:
            _id = client.maindb.user.insert_one(dict(user))
            return userEntity(client.maindb.user.find_one({"_id": ObjectId(str(_id.inserted_id))}))
        else:
            return -2  # existe cadastro com esse login
    else:
        return -1  # existe cadastro com esse cpf/cnpj
        

@ userAPI.put('/updateUser/{id}')
# Update a usera by ID
async def updateUser(id, user: User):
    try:
        user.password = pwd_cxt.hash(user.password)
        client.maindb.user.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": dict(user)})
        return userEntity(client.maindb.user.find_one({"_id": ObjectId(id)}))
    except:
        return dict([])


@ userAPI.delete('/delUser/{id}')
# Delete a user by ID
async def deleteUser(id):
    try:
        return usersEntity(client.maindb.user.find_one_and_delete({"_id": ObjectId(id)}))
    except:
        return dict([])
