from typing import Dict, Union

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

import config
import dictionary
from categories.category_admin import CategoryAdmin
from categories.category_user import CategoryUser
from dbmanager import DataBaseManager
from keyboards import keyboards_admin, keyboards_general
from states.states_admin import CategoryStatesAdmin


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
        await message.answer(dictionary.CHOOSE_CATEGORY, reply_markup=keyboard)

    ######################################################################################
    ######################################################################################

    async def create_subcategory_admin(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        category = self.get_object_category(data['category'])

        path = await category.get_path(state)

        if await self.db.get_data(data['category'], path) \
                or (await category.check_data_in_subcategories(path) and category.subcategories_is_object) \
                or not category.with_subcategories:
            await message.answer('Здесь нельзя создать новый подкаталог')
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

    ######################################################################################
    ######################################################################################

    async def edit_subcategory_admin(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        category = self.get_object_category(data['category'])

        path = await category.get_path(state)

        if await self.db.get_data(data['category'], path) \
                or (await category.check_data_in_subcategories(path) and category.subcategories_is_object) \
                or not category.with_subcategories:
            await message.answer('Здесь нельзя изменять подкаталог')
            return

        await state.set_state(CategoryStatesAdmin.EditOldName)

        subcategories = await self.db.get_subcategories(category.name_button, path)

        keyboard = keyboards_general.cancel_keyboard()
        keyboard = keyboards_admin.with_subcategories_keyboard(keyboard, subcategories)
        await message.answer('Выберите подкаталог для изменения', reply_markup=keyboard)

    async def edit_old_subcategory_admin(self, message: types.Message, state: FSMContext):
        old_name = message.text

        data = await state.get_data()
        category = self.get_object_category(data['category'])

        path = await category.get_path(state)

        subcategories = await self.db.get_subcategories(category.name_button, path)

        if old_name not in subcategories:
            await message.answer('Данный подкаталог не найдена')
            return

        await state.update_data(old_name=old_name)
        await state.set_state(CategoryStatesAdmin.EditNewName)

        keyboard = keyboards_general.cancel_keyboard()
        await message.answer('Введите новое название для подкаталога', reply_markup=keyboard)

    async def edit_new_subcategory_admin(self, message: types.Message, state: FSMContext):
        new_name = message.text

        data = await state.get_data()
        category = self.get_object_category(data['category'])

        path = await category.get_path(state)
        subcategories = await self.db.get_subcategories(category.name_button, path)

        if new_name in subcategories:
            await message.answer('Подкаталог с таким названием уже создан')
            return

        await state.update_data(new_name=new_name)
        await state.set_state(CategoryStatesAdmin.EditConfirm)

        data = await state.get_data()

        text = f'Старое название: {data["old_name"]} \n' \
               f'Новое название: {data["new_name"]}'
        await message.answer(text)

        keyboard = keyboards_general.confirm_cancel_keyboard()
        await message.answer('Вы действительно хотите изменить название каталога?', reply_markup=keyboard)

    async def edit_confirm_subcategory_admin(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        category = self.get_object_category(data['category'])

        path = await category.get_path(state)

        await self.db.edit_subcategory(category.name_button, path, data['old_name'], data['new_name'])

        await message.answer('Успешно изменено название подкатегории')

        await category.move_admin(message, state, path)

    ######################################################################################
    ######################################################################################

    async def delete_subcategory_admin(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        category = self.get_object_category(data['category'])

        path = await category.get_path(state)

        if await self.db.get_data(data['category'], path) \
                or (await category.check_data_in_subcategories(path) and category.subcategories_is_object) \
                or not category.with_subcategories:
            await message.answer('Здесь нельзя удалять подкаталог')
            return

        await state.set_state(CategoryStatesAdmin.DeleteSubcategory)

        subcategories = await self.db.get_subcategories(category.name_button, path)

        keyboard = keyboards_general.cancel_keyboard()
        keyboard = keyboards_admin.with_subcategories_keyboard(keyboard, subcategories)
        await message.answer('Выберите подкаталог для удаления', reply_markup=keyboard)

    async def delete_name_subcategory_admin(self, message: types.Message, state: FSMContext):
        name = message.text

        data = await state.get_data()
        category = self.get_object_category(data['category'])

        path = await category.get_path(state)

        subcategories = await self.db.get_subcategories(category.name_button, path)

        if name not in subcategories:
            await message.answer('Данный подкаталог не найдена')
            return

        await state.update_data(name=name)
        await state.set_state(CategoryStatesAdmin.DeleteSubcategoryConfirm)

        text = f'Название каталога: {name} '
        await message.answer(text)

        keyboard = keyboards_general.confirm_cancel_keyboard()
        await message.answer('Вы действительно хотите удалить данный каталога?', reply_markup=keyboard)

    async def delete_confirm_subcategory_admin(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        category = self.get_object_category(data['category'])

        path = await category.get_path(state)

        await self.db.delete_subcategory(category.name_button, path, data['name'])

        await message.answer('Успешно удален подкаталог')

        await category.move_admin(message, state, path)

    ######################################################################################
    ######################################################################################

    async def cancel_admin(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        category = self.get_object_category(data['category'])

        if category is not None:
            await category.cancel_admin(message, state)

    async def load_categories(self, message: types.Message, state: FSMContext):
        for category in self._categories.values():
            if not await self.db.check_category(category.name_button):
                await self.db.create_category(category.name_button)

    def get_object_category(self, category_name: str):
        return self._categories.get(category_name, None)

    def register_admin_command_events(self, dp: Dispatcher):
        dp.register_message_handler(self.main_menu, commands=['admin'], state='*')

    def register_admin_events(self, dp: Dispatcher):
        dp.register_message_handler(self.cancel_admin, Text(dictionary.CANCEL), state=CategoryStatesAdmin.states)
        dp.register_message_handler(self.main_menu, Text(dictionary.MAIN_MENU), state=CategoryStatesAdmin.states)
        dp.register_message_handler(self.load_categories, Text(dictionary.LOAD_CATEGORIES),
                                    state=CategoryStatesAdmin.ChooseCategory)

        dp.register_message_handler(self.name_new_subcategory_admin, content_types=ContentType.TEXT,
                                    state=CategoryStatesAdmin.CreateSubcategory)

        dp.register_message_handler(self.edit_old_subcategory_admin, content_types=ContentType.TEXT,
                                    state=CategoryStatesAdmin.EditOldName)
        dp.register_message_handler(self.edit_new_subcategory_admin, content_types=ContentType.TEXT,
                                    state=CategoryStatesAdmin.EditNewName)
        dp.register_message_handler(self.edit_confirm_subcategory_admin, Text(dictionary.CONFIRM),
                                    state=CategoryStatesAdmin.EditConfirm)

        dp.register_message_handler(self.delete_name_subcategory_admin, content_types=ContentType.TEXT,
                                    state=CategoryStatesAdmin.DeleteSubcategory)
        dp.register_message_handler(self.delete_confirm_subcategory_admin, Text(dictionary.CONFIRM),
                                    state=CategoryStatesAdmin.DeleteSubcategoryConfirm)

        for category in self._categories.values():
            category.register_admin_events(dp)
