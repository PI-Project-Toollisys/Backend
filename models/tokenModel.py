from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: int


class TokenData(BaseModel):
    login: Optional[str] = None
