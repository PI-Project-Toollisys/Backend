from typing import List


def ipAttackEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "firm": str(item["firm"]),
        "date": str(item["date"]),
        "ip_list": item["ip_list"],
        "method": str(item["method"]),
        "results": str(item["results"]),
        "ip_invalid_list": item["ip_invalid_list"],
        "ip_proxy_test_list": item["ip_proxy_test_list"],
    }


def ipAttacksEntity(entity) -> list:
    return [ipAttackEntity(item) for item in entity]
