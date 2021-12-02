from pydantic import BaseModel


class IpAttack(BaseModel):
    firm: str
    date: str
    listIp: list = []
    port: int
    numReq: int
    numProcess: int
    process: list = []

class postAttack(BaseModel):
    firm: str
    date: str
    listIp: list = []
    port: int
    numReq: int
    numProcess: int
    process: list = []
