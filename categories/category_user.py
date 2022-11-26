from typing import List

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import dictionary
from categories.category_general import Category
from keyboards import keyboards_user


class CategoryUser(Category):
    def __init__(self, smg_bot, name_button: str, user_states, admin_states,
                 create_button: str = None, edit_button: str = None, delete_button: str = None,
                 msg_choice: str = None, with_subcategories: bool = True, subcategories_is_object: bool = True):
        super().__init__(smg_bot, name_button, user_states, admin_states, create_button, edit_button, delete_button,
                         msg_choice, with_subcategories, subcategories_is_object)

    async def select_category_user(self, message: types.Message, state: FSMContext):
        await self.move_user(message, state, [])

    async def subcategories_user(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        subcategory_next = message.text

        if subcategory_next not in await self.smg_bot.db.get_subcategories(self.name_button, path):
            await message.answer(dictionary.NO_SUBCATEGORY)
            return

        path.append(message.text)

        await self.move_user(message, state, path)

    async def cancel_user(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        await state.reset_data()

        await self.move_user(message, state, path)

    async def back_user(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        if len(path) == 0:
            await self.smg_bot.handler_user.main_menu(message, state)
            return

        path.pop(-1)

        await state.reset_data()

        await self.move_user(message, state, path)

    async def move_user(self, message: types.Message, state: FSMContext, path: List[str]):
        if subcategories := await self.smg_bot.db.get_subcategories(self.name_button, path):
            await state.set_state(self.user_states.Chosen)
            await state.update_data(category=self.name_button, path=path)

            keyboard = keyboards_user.subcategory_keyboard(subcategories, path)
            text = self.msg_choice if await self.check_data_in_subcategories(path) else dictionary.CHOOSE_SUBCATEGORY

            await message.answer(text , reply_markup=keyboard)

        else:
            await self.event_user(message, state)

    async def event_user(self, message: types.Message, state: FSMContext):
        pass

    def register_user_events(self, dp: Dispatcher):
        dp.register_message_handler(self.smg_bot.handler_user.main_menu, Text(dictionary.MAIN_MENU),
                                    state=self.user_states)
        dp.register_message_handler(self.back_user, Text(dictionary.BACK), state=self.user_states)
        dp.register_message_handler(self.cancel_user, Text(dictionary.CANCEL), state=self.user_states)

        dp.register_message_handler(self.select_category_user, Text(self.name_button),
                                    state=self.user_states.ChooseCategory)
        dp.register_message_handler(self.subcategories_user, state=self.user_states.Chosen)
