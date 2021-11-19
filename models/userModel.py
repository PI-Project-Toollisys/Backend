from pydantic import BaseModel


class User(BaseModel):
    name: str
    login: str
    password: str
    permission: int
    firm: str  # cnpj
    register_identifier: str  # cpf or cnpj
