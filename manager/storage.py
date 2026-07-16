import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

USERS = BASE_DIR / 'users'
USERS.mkdir(exist_ok=True)

FAMILY = BASE_DIR / 'family.json'


def get_file(user_id, family):
    if family:
        return FAMILY
    return USERS / f"user_{user_id}.json"


def load_data(user_id, family):
    file = get_file(user_id, family)
    try:
        with open(file, 'r', encoding='utf-8') as open_file:
            return json.load(open_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_data(data, user_id, family):
    file = get_file(user_id, family)
    with open(file, 'w', encoding='utf-8') as write_file:
        json.dump(data, write_file, indent=4, ensure_ascii=False)
