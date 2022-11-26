from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

import dictionary
from categories.categories import AboutBot
from keyboards import keyboards_general
from states.states_admin import AboutBotStatesAdmin


class AboutBotAdmin(AboutBot):
    def __init__(self, smg_bot):
        super().__init__(smg_bot)

        self.admins_states = AboutBotStatesAdmin

    async def event_admin(self, message: types.Message, state: FSMContext):
        data_db = await self.smg_bot.db.get_data(self.name_button)

        description = data_db.get('description')

        text = f'Текущий описание Бота: \n' \
               f'{description}'

        keyboard = self.get_action_object_keyboard()
        await message.answer(text, reply_markup=keyboard)

    async def edit_object_admin(self, message: types.Message, state: FSMContext):
        await state.set_state(self.admins_states.EditDescription)

        keyboard = keyboards_general.cancel_keyboard()
        await message.answer('Напишите в одном сообщении новое описание Бота', reply_markup=keyboard)

    async def edit_description_admin(self, message: types.Message, state: FSMContext):
        description = message.text

        await state.update_data(description=description)
        await state.set_state(self.admins_states.EditConfirm.state)

        text = f'Вы действительно хотите изменить текущее описание Бота на это: \n' \
               f'{description}'
        keyboard = keyboards_general.confirm_cancel_keyboard()
        await message.answer(text, reply_markup=keyboard)

    async def edit_confirm_admin(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        path = data['path']

        data_db = {'description': data['description']}

        await self.smg_bot.db.set_data(self.name_button, path, data_db)

        await message.answer('Успешно изменено описание Бота')

        await self.cancel_admin(message, state)

    def register_admin_events(self, dp: Dispatcher):
        super().register_admin_events(dp)

        dp.register_message_handler(self.edit_description_admin, content_types=ContentType.TEXT,
                                    state=self.admins_states.EditDescription)
        dp.register_message_handler(self.edit_confirm_admin, Text(dictionary.CONFIRM),
                                    state=self.admins_states.EditConfirm)
