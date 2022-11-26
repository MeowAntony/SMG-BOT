from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import dictionary
from keyboards import keyboards_general


def categories_keyboard(categories):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for category in categories:
        keyboard.add(KeyboardButton(category))

    return keyboard

def subcategory_keyboard(subcategories: List[str], path: List[str] = None):
    keyboard = keyboards_general.return_keyboard(path)

    for subcategory in subcategories:
        keyboard.add(KeyboardButton(subcategory))

    return keyboard

def regulations_answer(is_not_actually=True):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(dictionary.MAIN_MENU))
    keyboard.add(KeyboardButton('Выбрать другой'))
    if is_not_actually:
        keyboard.add(KeyboardButton('Документ не актуальный'))

    return keyboard

def faq_answer(is_not_ask=True):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(dictionary.MAIN_MENU))
    keyboard.add(KeyboardButton('Выбрать другой'))
    if is_not_ask:
        keyboard.add(KeyboardButton('Не удовлетворён'))

    return keyboard
