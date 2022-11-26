from typing import List

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from dbmanager import DataBaseManager
from states.states_admin import AdminStates


class AdminSubcategoriesHandler:
    def __init__(self, db, categories, keyboards):

        self.db: DataBaseManager = db
        self._categories = categories
        self.keyboards = keyboards

    async def create_subcategory(self, message: Message, state: FSMContext):
        data = await state.get_data()
        category_name = data['category']
        path = data['path']

        if category := self.get_category_object(category_name) is None:
            await message.answer('Нельзя создать подкаталог среди главных каталогов')
            return

        if len(path) == 0 and not category.with_subcategories:
            await message.answer('Нельзя создать подкаталог в этом каталоге')
            return

        subcategories = await self.db.get_subcategories(category.name, path)

    def get_category_object(self, category_name):
        for category in self._categories:
            if category.name == category_name:
                return category
        else:
            return None

    def register_subcategories_events(self, dp: Dispatcher):
        dp.register_message_handler(self.create_subcategory, Text('Создать подкатегорию'), state=AdminStates.states)
        dp.register_message_handler(self.main_menu, Text('Изменить подкатегорию'), state=AdminStates.states)
        dp.register_message_handler(self.main_menu, Text('Удалить подкатегорию'), state=AdminStates.states)
