from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards import keyboards_general


def categories_keyboard(categories):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for category in categories:
        keyboard.add(KeyboardButton(category))

    return keyboard


def action_subcategory_keyboard(subcategories: List[str], path: List[str]):
    keyboard = keyboards_general.return_keyboard(path)

    keyboard.row(KeyboardButton('Создать подкаталог'),
                 KeyboardButton('Изменить подкаталог'),
                 KeyboardButton('Удалить подкаталог'))

    for subcategory in subcategories:
        keyboard.add(KeyboardButton(subcategory))

    return keyboard


def action_object_subcategories_keyboard(keyboard: ReplyKeyboardMarkup, subcategories=None):
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

    keyboard.add('Создать подкаталог')

    return keyboard


def create_object_subcategory_keyboard(create_button: str, path: List[str]):
    keyboard = keyboards_general.return_keyboard(path)

    keyboard.row(KeyboardButton('Создать подкаталог'), KeyboardButton(create_button))

    return keyboard
