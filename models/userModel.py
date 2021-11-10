from pydantic import BaseModel


class User(BaseModel):
    name: str
    login: str
    password: str
    permission: int
    firm: str  # cnpj
    register_identifier: int  # cpf or cnpj
