import json
import requests

from services.constants import BASE_URL, TAGS_URL


def get_all_tags(token: str):
    r = requests.get(url=f'{BASE_URL}{TAGS_URL}',
                     cookies={'access_token': token})

    result = r.json()
    return result
