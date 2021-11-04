from pydantic import BaseModel


class Firm(BaseModel):
    cnpj: str
    name: str
    status: str
    phone: int
    cep: int
    main_activity: str
    fantasy_name: str
