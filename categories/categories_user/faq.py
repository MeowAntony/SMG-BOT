from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

import config
import dictionary
from categories.categories import FAQ
from keyboards import keyboards_user, keyboards_general
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

    async def ask_question_user(self, message: types.Message, state: FSMContext):
        await state.set_state(self.user_states.QuestionGet)

        await message.answer("Напишите в одном сообщение вопрос, который у вас возник")

    async def get_question_user(self, message: types.Message, state: FSMContext):
        question = message.text

        await state.update_data(question=question)
        await state.set_state(self.user_states.QuestionSendConfirm.state)

        keyboard = keyboards_general.confirm_cancel_keyboard()
        await message.answer(f'Вы действительно хотите отправить это сообщение:\n'
                             f'{question}', reply_markup=keyboard)

    async def confirm_question_user(self, message: types.Message, state: FSMContext):
        user = message.from_user

        data = await state.get_data()
        question = data['question']

        text = f'Пользователь {user.first_name} {user.last_name} (@{user.username}, id{user.id}) ' \
               f'задал вопрос через FAQ. \n' \
               f'Вопрос: {question}'

        await self.smg_bot.bot.send_message(config.MAIN_ADMIN, text=text)

        keyboard = keyboards_user.faq_answer(is_not_ask=False)
        await message.answer('Ваше сообщение успешно доставлено администратору', reply_markup=keyboard)

    def register_user_events(self, dp: Dispatcher):
        super().register_user_events(dp)

        dp.register_message_handler(self.ask_question_user, Text('Ответ не удовлетворил'),
                                    state=self.user_states.QuestionSelected)
        dp.register_message_handler(self.get_question_user, content_types=ContentType.TEXT,
                                    state=self.user_states.QuestionGet)
        dp.register_message_handler(self.confirm_question_user, Text(dictionary.CONFIRM),
                                    state=self.user_states.QuestionSendConfirm)

        dp.register_message_handler(self.back_user, Text('Выбрать другой вопрос'),
                                    state=self.user_states.QuestionSelected)
