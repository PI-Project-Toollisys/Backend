from pydantic import BaseModel


class IpAttack(BaseModel):
    firm: str
    date: str
    process: list = []

class postAttack(BaseModel):
    firm: str
    date: str
    host: str
    port: int
    listIp: list = []
    numReq: int
    numProcess: int
