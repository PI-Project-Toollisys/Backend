def answerEntity(item) -> dict:
    return{
        "id": str(item["_id"]),
        "firm": str(item["firm"]),
        "date": str(item["date"]),
        "rec": item["rec"],
        "arm": item["arm"],
        "ent": item["ent"],
        "exp": item["exp"],
        "ins": item["ins"],
        "com": item["com"],
        "aca": item["aca"],
        "inft": item["inft"],
        "infm": item["infm"],
        "dad": item["dad"]
    }


def answersEntity(entity) -> list:
    return [answerEntity(item) for item in entity]
