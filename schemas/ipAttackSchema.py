from typing import List


def ipAttackEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "firm": str(item["firm"]),
        "date": str(item["date"]),
        "listIp":item["listIp"],
        "port":int(item["port"]),
        "numReq":int(item["numReq"]),
        "numProcess":int(item["numProcess"]),
        "process": item["process"],
    }


def ipAttacksEntity(entity) -> list:
    return [ipAttackEntity(item) for item in entity]
