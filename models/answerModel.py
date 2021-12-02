from pydantic import BaseModel

class Answer(BaseModel):
    firm: str
    date: str
    rec: dict = {}
    arm: dict = {}
    ent: dict = {}
    exp: dict = {}
    ins: dict = {}
    com: dict = {}
    aca: dict = {}
    inft: dict = {}
    infm: dict = {}
    dad: dict = {}
