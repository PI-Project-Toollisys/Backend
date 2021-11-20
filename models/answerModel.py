from pydantic import BaseModel

class Answer(BaseModel):
    firm: str
    date: str
    rec1: list = []
    rec2: list = []
    rec3: list = []
    rec4: list = []
    rec5: list = []
    arm1: list = []
    arm2: list = []
    arm3: list = []
    ent1: list = []
    ent2: list = []
    ent3: list = []
    ent4: list = []
    ent5: list = []
    exp1: list = []
    exp2: list = []
    exp3: list = []
    ins1: list = []
    ins2: list = []
    ins3: list = []
    com1: list = []
    com2: list = []
    com3: list = []
    aca1: list = []
    aca2: list = []
    aca3: list = []
    inf1: list = []
    inf2: list = []
    inf3: list = []
    inf4: list = []
    int1: list = []
    int2: list = []
    int3: list = []
    dad1: list = []
    dad2: list = []
    dad3: list = []
