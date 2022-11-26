from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

import dictionary
from categories.categories import ITRequests
from keyboards import keyboards_general
from states.states_user import ITRequestsStatesUser


class ITRequestsUser(ITRequests):
    def __init__(self, smg_bot):
        super().__init__(smg_bot)

        self.user_states = ITRequestsStatesUser

    # TODO сделать
    async def event_user(self, message: types.Message, state: FSMContext):
        #if not (data_db := await self.smg_bot.db.get_data(self.name_button)):
        #    await message.answer('Попросите администратора настроить данный каталог')
         #   return

        #text = data_db['info']

        text = "Напишите в одном сообщение заявку в IT. Она будет отправлена на почту."

        await state.set_state(self.user_states.SendMessage.state)

        keyboard = keyboards_general.return_keyboard()
        await message.answer(text=text, reply_markup=keyboard)

    async def send_message_email_user(self, message: types.Message, state: FSMContext):
        text = message.text

        await state.update_data(text=text)
        await state.set_state(self.user_states.SendConfirm.state)

        keyboard = keyboards_general.confirm_cancel_keyboard()
        await message.answer(f'Вы действительно хотите отправить это сообщение на почту:\n'
                             f'{text}', reply_markup=keyboard)

    async def send_confirm(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        text = data['text']

        await self.send_email_message(self.smg_bot.sender_email, 'Смотри что чудит Анжелка с бухгалтерией', text)

        await message.answer('Ваше сообщение успешно доставлено на почту')

        await self.back_user(message, state)

    def register_user_events(self, dp: Dispatcher):
        super().register_user_events(dp)

        dp.register_message_handler(self.send_message_email_user, content_types=ContentType.TEXT,
                                    state=self.user_states.SendMessage)
        dp.register_message_handler(self.send_confirm, Text(dictionary.CONFIRM),
                                    state=self.user_states.SendConfirm)
