from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import config
from categories.categories import Regulations
from keyboards import keyboards_user
from states.states_user import RegulationsStatesUser


class RegulationsUser(Regulations):
    def __init__(self, smg_bot):
        super().__init__(smg_bot)
        self.user_states = RegulationsStatesUser

    async def event_user(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state) + message.text

        if not (data_db := await self.smg_bot.db.get_data(self.name_button, path)):
            return

        document = data_db['document']

        await state.update_data(path=path)
        await state.set_state(self.user_states.DocumentSelected)

        keyboard = keyboards_user.regulations_answer()
        await message.answer_document(document=document, reply_markup=keyboard)

    async def wrong_document_user(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        user = message.from_user
        text = f'Пользователь {user.first_name} {user.last_name} (@{user.username}, id{user.id}) сообщил,' \
               f'что нормативный документ не актуален. \n\n' \
               f'Путь до документа: "{self.name_button} -> {"->".join(path)}"'
        await self.smg_bot.bot.send_message(config.MAIN_ADMIN, text=text)

        keyboard = keyboards_user.regulations_answer(is_not_actually=False)
        await message.answer("Успешно оповестили о том, что документ не актуален.", reply_markup=keyboard)

    def register_user_events(self, dp: Dispatcher):
        super().register_user_events(dp)
        
        dp.register_message_handler(self.wrong_document_user, Text('Документ не актуальный'),
                                    state=self.user_states.DocumentSelected)

        dp.register_message_handler(self.back_user, Text('Выбрать другой'),
                                    state=self.user_states.DocumentSelected)
