import json
import requests
from services.constants import BASE_URL, NOTES_URL

# Запрос для получения всех заметок


def get_all_notes(token: str, tg_id: int):
    r = requests.get(url=f'{BASE_URL}{NOTES_URL}',
                     cookies={'access_token': token},
                     params={'tg_id': tg_id})

    result = r.json()
    return result

# Запрос для получения всех заметок указанного тега


def get_notes_by_tag(token: str, tg_id: int, tag_id: int):
    r = requests.get(url=f'{BASE_URL}{NOTES_URL}',
                     cookies={'access_token': token},
                     params={'tg_id': tg_id, 'tag_id': tag_id})

    result = r.json()
    return result

# Запрос для создания заметок


def create_note(token: str, data: dict[str, str | int | list[str]]):
    payload = {
        'title': data['title'],
        'content': data['content'],
        'tg_id': data['tg_id'],
        'tags': data['tags']
    }

    r = requests.post(url=f'{BASE_URL}{NOTES_URL}',
                      cookies={'access_token': token},
                      data=json.dumps(payload))

    result = r.json()
    return result
