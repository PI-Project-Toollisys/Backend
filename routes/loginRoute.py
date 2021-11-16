from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from conf.db import client

# from models.loginModel import Login
from authentication.token import create_access_token
from schemas.userSchema import userEntity

from passlib.context import CryptContext
pwd_cxt =CryptContext(schemes=["bcrypt"],deprecated="auto")

loginAPI = APIRouter(tags=['Login'])


@loginAPI.post('/login')
async def login(loginP: OAuth2PasswordRequestForm = Depends()):
    try:
        user = userEntity(client.maindb.user.find_one({"login": loginP.username}))
    except:
        raise HTTPException(status_code=404, detail="Invalid Login 1")

    if not pwd_cxt.verify(loginP.password, user["password"]):
        raise HTTPException(status_code=404, detail="Invalid Login 2")

    access_token = create_access_token(data={"sub": user['login']})
    return {"access_token": access_token, "token_type": user["permission"]}
