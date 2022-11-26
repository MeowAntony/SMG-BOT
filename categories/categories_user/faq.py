from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import dictionary
from categories.categories import FAQ
from keyboards import keyboards_user
from states.states_user import FAQStatesUser


class FAQUser(FAQ):
    def __init__(self, smg_bot):
        super().__init__(smg_bot)

        self.user_states = FAQStatesUser

    async def event_user(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state) + [message.text]

        if not (data_db := await self.smg_bot.db.get_data(self.name_button, path)):
            return

        text = data_db['answer']

        await state.update_data(path=path)
        await state.set_state(self.user_states.QuestionSelected)

        keyboard = keyboards_user.faq_answer()
        await message.answer(text, reply_markup=keyboard)

    async def move_to_answer_user(self, message: types.Message, state: FSMContext):
        data_db = await self.smg_bot.db.get_data(self.name_button)

        category_name_answer = data_db.get('category_answer', None)
        path_answer = data_db.get('path_answer', None)

        if category_name_answer is None or path_answer is None:
            await message.answer('Невозможно перейти к ответу')
            return

        await self.smg_bot.handler_user.get_object_category(category_name_answer).move_user(message, state, path_answer)

    async def ask_question_user(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)
        # TODO
        user = message.from_user
        text = f'Пользователь {user.first_name} {user.last_name} (@{user.username}, id{user.id}) сообщил,' \
               f'что нормативный документ не актуален. \n\n' \
               f'Путь до документа: "{self.name_button} -> {"->".join(path)}"'
        await self.smg_bot.bot.send_message(config.MAIN_ADMIN, text=text)

        keyboard = keyboards_user.regulations_answer(is_not_actually=False)
        await message.answer("Успешно оповестили о том, что документ не актуален.", reply_markup=keyboard)

    def register_user_events(self, dp: Dispatcher):
        super().register_user_events(dp)

        dp.register_message_handler(self.move_to_answer_user, Text(dictionary.MOVE),
                                    state=self.user_states.QuestionSelected)

        dp.register_message_handler(self.back_user, Text('Выбрать другой'),
                                    state=self.user_states.QuestionSelected)
