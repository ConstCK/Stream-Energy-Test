import requests

from ..utils.constants import USER_URL


def register(user_id: int):
    r = requests.post(url=USER_URL, data=user_id)
