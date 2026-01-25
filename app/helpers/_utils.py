from fastapi import HTTPException
import app.db as db
import copy


def hash_password(password: str):
    password = password.lower()
    result = []

    for char in password:
        if char.isalpha():
            num = ord(char) - ord('a') + 1
            result.append(str(num))
        else:
            result.append(char)

    return "-".join(result)


def email_exists(email: str):
    return any(u["email"].lower() == email.lower() for u in db.users)


def get_scenario_or_404(scenario_id: int, user_id: int):
    scenario = next(
        (s for s in db.scenarios if s["id"] == scenario_id and s["owner_id"] == user_id),
        None
    )
    if scenario is None:
        raise HTTPException(
            404,
            {"code": "SCENARIO_NOT_FOUND", "message": "Scenario does not exist for this user."}
        )
    return scenario


def ensure_owner(scenario: dict, user_id: int):
    if scenario["owner_id"] != user_id:
        raise HTTPException(
            403,
            {"code": "NOT_OWNER", "message": "You do not own this scenario."}
        )


def clone_template(template: dict, user_id: int):
    new_scenario = copy.deepcopy(template)
    new_scenario["owner_id"] = user_id
    return new_scenario