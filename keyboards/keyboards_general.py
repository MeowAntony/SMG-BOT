from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import dictionary


def cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(KeyboardButton('Отмена'))

    return keyboard


def back_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(KeyboardButton('Назад'))

    return keyboard


def return_keyboard(path=None) -> ReplyKeyboardMarkup:
    if path is None:
        path = []

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    if len(path) == 0:
        keyboard.add(KeyboardButton('Главное меню'))
    else:
        keyboard.row(KeyboardButton('Главное меню'), KeyboardButton('Назад'))

    return keyboard


def confirm_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton('Подтвердить'), KeyboardButton('Отмена'))

    return keyboard


def skip_cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(KeyboardButton(dictionary.SKIP), KeyboardButton('Отмена'))

    return keyboard


def continue_cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(KeyboardButton(dictionary.CONTINUE), KeyboardButton('Отмена'))

    return keyboard
