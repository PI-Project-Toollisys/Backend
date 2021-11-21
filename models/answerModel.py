from pydantic import BaseModel

class Answer(BaseModel):
    firm: str
    date: str
    rec: list = []
    arm: list = []
    ent: list = []
    exp: list = []
    ins: list = []
    com: list = []
    aca: list = []
    inft: list = []
    infm: list = []
    dad: list = []
