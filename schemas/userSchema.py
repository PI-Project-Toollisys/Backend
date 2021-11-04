def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": str(item["name"]),
        "login": str(item["login"]),
        "password": str(item["password"]),
        "permission": int(item["permission"]),
        "firm": str(item["firm"]),
        "register_identifier": int(item["register_identifier"])
    }


def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]
