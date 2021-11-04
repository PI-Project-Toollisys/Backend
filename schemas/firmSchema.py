def firmEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "cnpj": str(item["cnpj"]),
        "name": str(item["name"]),
        "status": str(item["status"]),
        "phone": int(item["phone"]),
        "cep": int(item["cep"]),
        "main_activity": str(item["main_activity"]),
        "fantasy_name": str(item["fantasy_name"])
    }


def firmsEntity(entity) -> list:
    return [firmEntity(item) for item in entity]
