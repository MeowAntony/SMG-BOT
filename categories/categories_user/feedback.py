from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

import config
import dictionary
from categories.categories import Feedback
from keyboards import keyboards_general
from states.states_user import FeedbackStatesUser


class FeedbackUser(Feedback):
    def __init__(self, smg_bot):
        super().__init__(smg_bot)

        self.user_states = FeedbackStatesUser

    async def event_user(self, message: types.Message, state: FSMContext):
        if not (data_db := await self.smg_bot.db.get_data(self.name_button)):
            await message.answer('Попросите администратора настроить данный каталог')
            return

        text = data_db['info']

        await state.set_state(self.user_states.SendMessage.state)

        keyboard = keyboards_general.return_keyboard()
        await message.answer(text=text, reply_markup=keyboard)

    async def send_message_user(self, message: types.Message, state: FSMContext):
        text = message.text

        await state.update_data(text=text)
        await state.set_state(self.user_states.SendConfirm.state)

        keyboard = keyboards_general.confirm_keyboard()
        await message.answer(f'Вы действительно хотите отправить это сообщение:\n'
                             f'{text}', reply_markup=keyboard)

    async def send_confirm_user(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        text = data['text']

        user = message.from_user
        text = f'Пользователь {user.first_name} {user.last_name} (@{user.username}, id{user.id}) отправил сообщение ' \
               f'через обратную связь. \n' \
               f'Сообщение: "{text}"'

        await self.smg_bot.bot.send_message(config.MAIN_ADMIN, text=text)

        await message.answer('Ваше сообщение успешно доставлено администратору')

        await self.back_user(message, state)

    def register_user_events(self, dp: Dispatcher):
        super().register_user_events(dp)

        dp.register_message_handler(self.send_message_user, content_types=ContentType.TEXT,
                                    state=self.user_states.SendMessage)
        dp.register_message_handler(self.send_confirm_user, Text(dictionary.CONFIRM),
                                    state=self.user_states.SendConfirm)
