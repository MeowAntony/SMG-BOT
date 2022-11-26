from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

import config
import dictionary
from categories.categories import Feedback
from keyboards import keyboards_general
from states.states_admin import FeedbackStatesAdmin


class FeedbackAdmin(Feedback):
    def __init__(self, smg_bot):
        super().__init__(smg_bot)

        self.admins_states = FeedbackStatesAdmin

    async def event_admin(self, message: types.Message, state: FSMContext):
        data_db = await self.smg_bot.db.get_data(self.name_button)

        info = data_db.get('info', None)

        text = f'Текущий информация: \n' \
               f'{info}'

        keyboard = self.get_action_object_keyboard()
        await message.answer(text, reply_markup=keyboard)

    async def edit_object_admin(self, message: types.Message, state: FSMContext):
        await state.set_state(self.admins_states.EditInfo)

        keyboard = keyboards_general.cancel_keyboard()
        await message.answer('Напишите в одном сообщении новую информацию, которая будет показываться пользователю '
                             'при выборе этого каталога', reply_markup=keyboard)

    async def edit_info_admin(self, message: types.Message, state: FSMContext):
        info = message.text

        await state.update_data(info=info)
        await state.set_state(self.admins_states.EditConfirm.state)

        data = await state.get_data()

        text = f'Вы действительно хотите изменить текущее информацию на эту: \n' \
               f'{data["info"]}'

        keyboard = keyboards_general.confirm_keyboard()
        await message.answer(text, reply_markup=keyboard)

    async def edit_confirm_admin(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        path = data['path']

        data_db = {'info': data['info']}

        await self.smg_bot.db.set_data(self.name_button, path, data_db)

        await message.answer('Успешно изменена информация')

        await self.cancel_admin(message, state, path)

    def register_admin_events(self, dp: Dispatcher):
        super().register_admin_events(dp)

        dp.register_message_handler(self.edit_info_admin, content_types=ContentType.TEXT,
                                    state=self.admins_states.EditInfo)
        dp.register_message_handler(self.edit_confirm_admin, Text(dictionary.CONFIRM),
                                    state=self.admins_states.EditConfirm)