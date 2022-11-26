from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# можно создать и подкатегорию, и контакт
async def subcategory_contacts_keyboard(path: List[str]):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboards_other = [KeyboardButton('Главное меню')]
    if len(path) != 0:
        keyboards_other.append(KeyboardButton('Назад'))
    keyboard.row(*keyboards_other)

    keyboard.add(KeyboardButton('Создать подкаталог'))
    keyboard.add(KeyboardButton('Добавить контакт'))

    return keyboard


# можно создать/изменить/удалить только контакт
async def contacts_keyboard(path: List[str], contacts: List[str] = None):
    if contacts is None:
        contacts = []
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboards_other = [KeyboardButton('Главное меню')]
    if len(path) != 0:
        keyboards_other.append(KeyboardButton('Назад'))
    keyboard.row(*keyboards_other)

    keyboards_util = []
    if contacts:
        keyboards_util.append(KeyboardButton('Удалить контакт'))
        keyboards_util.append(KeyboardButton('Изменить контакт'))
    keyboards_util.append(KeyboardButton('Создать контакт'))
    keyboard.row(*keyboards_util)

    for contact in contacts:
        keyboard.add(contact)

    return keyboard

