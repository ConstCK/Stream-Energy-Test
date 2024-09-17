import json
import requests

from services.constants import BASE_URL, USER_URL


def register_user(data: dict[str, str | int]) -> str | None:
    payload = {
        "username": data['name'],
        "password": data['password'],
        "tg_id": data['tg_id']
    }
    r = requests.post(url=f'{BASE_URL}{USER_URL}/signup',
                      data=json.dumps(payload))

    result = r.text
    return result


def login_user(data: dict[str, int | str]) -> str | None:
    payload = {
        "username": data['name'],
        "password": data['password'],
        "tg_id": data['tg_id']
    }

    r = requests.post(url=f'{BASE_URL}{USER_URL}/login',
                      data=json.dumps(payload))

    result = r.text
    return result
