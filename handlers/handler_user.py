from typing import Dict, Union

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from categories.category_admin import CategoryAdmin
from categories.category_user import CategoryUser
from dbmanager import DataBaseManager
from keyboards import keyboards_user
from states.states_user import CategoryStatesUser, ALL_USER_STATES


class UserHandler:
    def __init__(self, db, categories):
        self.db: DataBaseManager = db
        self._categories: Dict[str, Union[CategoryUser, CategoryAdmin]] = categories

    async def main_menu(self, message: types.Message, state: FSMContext):
        await state.set_state(CategoryStatesUser.ChooseCategory)
        await state.set_data({'category': None, 'path': []})

        categories_names = self._categories.keys()
        keyboard = keyboards_user.categories_keyboard(categories_names)
        await message.answer('Выберите каталог', reply_markup=keyboard)

    def get_object_category(self, category_name: str):
        return self._categories.get(category_name, None)

    def register_user_command_events(self, dp: Dispatcher):
        dp.register_message_handler(self.main_menu, commands=['start'], state='*')

    def register_user_events(self, dp: Dispatcher):
        for category in self._categories.values():
            category.register_user_events(dp)
