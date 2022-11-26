from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

import dictionary
from categories.categories import FAQ
from keyboards import keyboards_general
from states.states_admin import FAQStatesAdmin


class FAQAdmin(FAQ):
    def __init__(self, smg_bot):
        super().__init__(smg_bot)

        self.admins_states = FAQStatesAdmin

    async def event_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state) + [message.text]

        if not (data_db := await self.smg_bot.db.get_data(self.name_button, path)):
            return

        text = data_db['answer']
        await message.answer(text)

    async def create_object_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        if not await self.check_can_create_object(path):
            await message.answer('Нельзя добавить вопрос, так где есть подкатегории')
            return

        await state.set_state(self.admins_states.CreateName)

        keyboard = keyboards_general.cancel_keyboard()
        await message.answer('Введите вопрос', reply_markup=keyboard)

    async def create_name_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        name = message.text

        if name in await self.smg_bot.db.get_subcategories(self.name_button, path):
            await message.answer('Введенное название уже существует в текущей подкатегории')
            return

        await state.update_data(name=name)
        await state.set_state(self.admins_states.CreateAnswer)

        await message.answer('Введите ответ на вопрос')

    async def create_answer_admin(self, message: types.Message, state: FSMContext):
        answer = message.text

        await state.update_data(answer=answer)

        await state.set_state(self.admins_states.CreateConfirm) # TODO сделать, чтобы можно было переходить

        data = await state.get_data()

        text = f'Вопрос: {data["name"]} \n' \
               f'Ответ: {data["answer"]}'
        await message.answer(text)

        keyboard = keyboards_general.confirm_cancel_keyboard()
        await message.answer('Вы действительно хотите создать данный вопрос?', reply_markup=keyboard)

    async def create_confirm_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        data = await state.get_data()
        data_db = {'answer': data['answer']}
        await self.smg_bot.db.create_subcategory(self.name_button, path, data['name'], data_db)

        await message.answer('Успешно создан вопрос с ответом')
        await self.cancel_admin(message, state)

    def register_admin_events(self, dp: Dispatcher):
        super().register_admin_events(dp)

        dp.register_message_handler(self.create_name_admin, content_types=ContentType.TEXT,
                                    state=self.admins_states.CreateName)
        dp.register_message_handler(self.create_answer_admin, content_types=ContentType.TEXT,
                                    state=self.admins_states.CreateAnswer)
        dp.register_message_handler(self.create_confirm_admin, Text(dictionary.CONFIRM),
                                    state=self.admins_states.CreateConfirm)
