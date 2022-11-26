from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import dictionary


def cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(KeyboardButton(dictionary.CANCEL))

    return keyboard


def back_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(KeyboardButton(dictionary.BACK))

    return keyboard


def return_keyboard(path=None) -> ReplyKeyboardMarkup:
    if path is None:
        path = []

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    if len(path) == 0:
        keyboard.add(KeyboardButton(dictionary.MAIN_MENU))
    else:
        keyboard.row(KeyboardButton(dictionary.MAIN_MENU), KeyboardButton(dictionary.BACK))

    return keyboard


def confirm_cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton(dictionary.CONFIRM),
                 KeyboardButton(dictionary.CANCEL))

    return keyboard


def skip_cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(KeyboardButton(dictionary.SKIP), KeyboardButton(dictionary.CANCEL))

    return keyboard


def continue_cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(KeyboardButton(dictionary.CONTINUE), KeyboardButton(dictionary.CANCEL))

    return keyboard
