from bson.objectid import ObjectId
from fastapi import APIRouter
from conf.db import client
from bson import ObjectId

from models.loginModel import Login
from schemas.loginSchema import loginEntity

loginAPI = APIRouter()


@loginAPI.get('/login')
async def login(login: Login):
    pass
