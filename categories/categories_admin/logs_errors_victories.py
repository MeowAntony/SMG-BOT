from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

import dictionary
from categories.categories import LogsErrorsVictories
from keyboards import keyboards_general
from states.states_admin import LogsErrorsVictoriesStatesAdmin


class LogsErrorsVictoriesAdmin(LogsErrorsVictories):
    def __init__(self, smg_bot):
        super().__init__(smg_bot)

        self.admins_states = LogsErrorsVictoriesStatesAdmin

    async def event_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state) + [message.text]

        if not (data_db := await self.smg_bot.db.get_data(self.name_button, path)):
            return

        text = data_db['text']

        await message.answer(text=text)

    async def create_object_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        if not await self.check_can_create_object(path):
            await message.answer('Нельзя добавить журнал, так где есть подкатегории')
            return

        await state.set_state(self.admins_states.CreateName)

        keyboard = keyboards_general.cancel_keyboard()
        await message.answer('Введите название журнала', reply_markup=keyboard)

    async def create_name_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        name = message.text

        if name in await self.smg_bot.db.get_subcategories(self.name_button, path):
            await message.answer('Введенное название уже существует в текущей подкатегории')
            return

        await state.update_data(name=name)
        await state.set_state(self.admins_states.CreateText)

        await message.answer('Введите ссылку или текст')

    async def create_text_admin(self, message: types.Message, state: FSMContext):
        text = message.text

        await state.update_data(text=text)
        await state.set_state(self.admins_states.CreateConfirm)

        data = await state.get_data()
        await message.answer(f'Название: {data["name"]}')

        await message.answer(data['text'])

        keyboard = keyboards_general.confirm_cancel_keyboard()
        await message.answer('Вы действительно хотите создать данный журнал?', reply_markup=keyboard)

    async def create_confirm_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        data = await state.get_data()
        data_db = {'text': data['text']}
        await self.smg_bot.db.create_subcategory(self.name_button, path, data['name'], data_db)

        await message.answer('Успешно создан журнал')
        await self.cancel_admin(message, state)

    def register_admin_events(self, dp: Dispatcher):
        super().register_admin_events(dp)

        dp.register_message_handler(self.create_name_admin, content_types=ContentType.TEXT,
                                    state=self.admins_states.CreateName)
        dp.register_message_handler(self.create_text_admin, content_types=ContentType.TEXT,
                                    state=self.admins_states.CreateText)
        dp.register_message_handler(self.create_confirm_admin, Text(dictionary.CONFIRM),
                                    state=self.admins_states.CreateConfirm)
