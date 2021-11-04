from pydantic import BaseModel


class IpAttack(BaseModel):
    firm: str
    date: str
    ip_list: list = []
    method: str
    results: str
    ip_invalid_list: list = []
    ip_proxy_test_list: list = []
