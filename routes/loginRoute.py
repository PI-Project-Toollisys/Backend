from datetime import timedelta
from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException
from conf.db import client
from bson import ObjectId

from models.loginModel import Login
from routes.token import create_access_token
from schemas.loginSchema import loginEntity
from schemas.userSchema import userEntity

from passlib.context import CryptContext
pwd_cxt =CryptContext(schemes=["bcrypt"],deprecated="auto")

loginAPI = APIRouter(tags=['Login'])


@loginAPI.post('/login')
async def login(login: Login):
    try:
        user = userEntity(client.maindb.user.find_one({"login": login.login}))
    except:
        raise HTTPException(status_code=404, detail="Invalid Login 1")

    if not pwd_cxt.verify(login.password, user['password']):
        raise HTTPException(status_code=404, detail="Invalid Login 2")

    access_token = create_access_token(data={"sub": user['register_identifier']})
    return {"access_token": access_token, "token_type": "bearer"}
