from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import dictionary
from keyboards import keyboards_general


def categories_keyboard(categories):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for category in categories:
        keyboard.add(KeyboardButton(category))

    keyboard.add(KeyboardButton(dictionary.LOAD_CATEGORIES))

    return keyboard


def action_subcategory_keyboard(subcategories: List[str], path: List[str]):
    keyboard = keyboards_general.return_keyboard(path)

    keyboard.row(KeyboardButton(dictionary.CREATE_SUBCATEGORY),
                 KeyboardButton(dictionary.EDIT_SUBCATEGORY),
                 KeyboardButton(dictionary.DELETE_SUBCATEGORY))

    for subcategory in subcategories:
        keyboard.add(KeyboardButton(subcategory))

    return keyboard


def with_subcategories_keyboard(keyboard: ReplyKeyboardMarkup, subcategories=None):
    if subcategories is None:
        subcategories = []

    for subcategory in subcategories:
        keyboard.add(KeyboardButton(subcategory))

    return keyboard

def get_action_object_keyboard(create_button: str = None, edit_button: str = None,
                               delete_button: str = None, path=None) -> ReplyKeyboardMarkup:
    if path is None:
        path = []

    keyboard = keyboards_general.return_keyboard(path)

    buttons_action = []
    for action_text in [create_button, edit_button, delete_button]:
        if action_text is not None:
            buttons_action.append(action_text)

    keyboard.row(*buttons_action)

    return keyboard

def create_subcategory():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(dictionary.CREATE_SUBCATEGORY)

    return keyboard


def create_object_subcategory_keyboard(create_button: str, path: List[str]):
    keyboard = keyboards_general.return_keyboard(path)

    keyboard.row(KeyboardButton(dictionary.CREATE_SUBCATEGORY), KeyboardButton(create_button))

    return keyboard
