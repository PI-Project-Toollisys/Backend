def loginEntity(item) -> dict:
    return {
        "login": str(item["login"]),
        "password": str(item["password"])
    }
