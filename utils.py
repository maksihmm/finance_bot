from aiogram.types import Message
from manager.storage import load_data, save_data


def get_storage(message: Message):
    user_id = message.from_user.id
    family = False

    return user_id, family


def load_user_operations(message: Message):
    user_id, family = get_storage(message)
    return load_data(user_id, family)


def save_user_operations(message: Message, operations):
    user_id, family = get_storage(message)
    save_data(operations, user_id, family)
