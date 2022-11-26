from typing import Dict, Union

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

import config
from categories.category_admin import CategoryAdmin
from categories.category_user import CategoryUser
from dbmanager import DataBaseManager
from keyboards import keyboards_admin, keyboards_general
from states.states_admin import CategoryStatesAdmin, ALL_ADMIN_STATES


class AdminHandler:
    def __init__(self, db, categories):

        self.db: DataBaseManager = db
        self._categories: Dict[str, Union[CategoryUser, CategoryAdmin]] = categories

    async def main_menu(self, message: types.Message, state: FSMContext):
        if message.from_user.id not in config.ADMINS:
            await message.answer('У вас нет доступа к панели администратора')
            return

        await state.set_state(CategoryStatesAdmin.ChooseCategory)
        await state.set_data({'category': None, 'path': []})

        categories = self._categories.keys()

        keyboard = keyboards_admin.categories_keyboard(categories)
        await message.answer('Выберите каталог', reply_markup=keyboard)

    async def create_subcategory_admin(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        category = self.get_object_category(data['category'])

        path = await category.get_path(state)

        if await self.db.get_data(data['category'], path) or not category.with_subcategories:
            await message.answer('Здесь нельзя создать новую подкаталог')
            return

        await state.set_state(CategoryStatesAdmin.CreateSubcategory)

        keyboard = keyboards_general.cancel_keyboard()
        await message.answer('Введите название подкаталога, который хотите создать', reply_markup=keyboard)

    async def name_new_subcategory_admin(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        category = self.get_object_category(data['category'])

        path = await category.get_path(state)

        subcategories = await self.db.get_subcategories(category.name_button, path)
        if message.text in subcategories:
            await message.answer('Подкаталог с таким названием уже создан. Введите новое название')
            return

        await self.db.create_subcategory(category.name_button, path, message.text)
        await message.answer(f'Успешно создан новый подкаталог: {message.text}')
        await category.move_admin(message, state, path)

    async def cancel_admin(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        category = self.get_object_category(data['category'])

        if category is not None:
            await category.cancel_admin(message, state)

    async def load_categories(self, message: types.Message):
        for category in self._categories.values():
            if not await self.db.check_category(category.name):
                await self.db.create_category(category.name)

    def get_object_category(self, category_name: str):
        return self._categories.get(category_name, None)

    def register_admin_command_events(self, dp: Dispatcher):
        dp.register_message_handler(self.main_menu, commands=['admin'], state='*')

    def register_admin_events(self, dp: Dispatcher):

        dp.register_message_handler(self.cancel_admin, Text('Отмена'), state=CategoryStatesAdmin.states)

        for category in self._categories.values():
            category.register_admin_events(dp)

        dp.register_message_handler(self.name_new_subcategory_admin, content_types=ContentType.TEXT,
                                    state=CategoryStatesAdmin.CreateSubcategory)
