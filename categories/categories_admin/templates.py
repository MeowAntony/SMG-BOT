from typing import List

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import MediaGroup, ContentType

import dictionary
from categories.categories import Templates
from keyboards import keyboards_general
from states.states_admin import TemplatesStatesAdmin

MAX_DOCUMENTS = 10


class TemplatesAdmin(Templates):
    def __init__(self, smg_bot):
        super().__init__(smg_bot)

        self.admins_states = TemplatesStatesAdmin

    async def event_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state) + [message.text]

        if not (data_db := await self.smg_bot.db.get_data(self.name_button, path)):
            return

        documents = data_db['documents']
        text = data_db['text']

        media_group = MediaGroup()
        for document in documents:
            media_group.attach_document(document)

        await message.answer_media_group(media_group)
        if text is not None:
            await message.answer(text)

    async def create_object_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        if not await self.check_can_create_object(path):
            await message.answer('Нельзя добавить шаблон, так где есть подкатегории')
            return

        await state.set_state(self.admins_states.CreateName)

        keyboard = keyboards_general.cancel_keyboard()
        await message.answer('Введите название шаблона', reply_markup=keyboard)

    async def create_name_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        name = message.text

        if name in await self.smg_bot.db.get_subcategories(self.name_button, path):
            await message.answer('Введенное название уже существует в текущей подкатегории')
            return

        await state.update_data(name=name)
        await state.set_state(self.admins_states.CreateDocument)

        keyboard = keyboards_general.cancel_keyboard()
        await message.answer('Прикрепите документы (от 1 до 10 штук). \n'
                             'Документы нужно прикреплять отдельными сообщениями',
                             reply_markup=keyboard)

    async def create_document_admin(self, message: types.Message, state: FSMContext):

        data = await state.get_data()
        documents = data.get('documents', [])

        if message.text == dictionary.CONTINUE:
            if len(documents) == 0:
                await message.answer('Нельзя продолжить. Вы не прикрепили ни одного документа')
                return
            else:
                await state.set_state(self.admins_states.CreateText)
                keyboard = keyboards_general.skip_cancel_keyboard()

                await message.answer('Введите текст (можно пропустить)', reply_markup=keyboard)
                return

        if len(documents) == MAX_DOCUMENTS:
            await message.answer(f'Уже добавлено максимальное количество документов ({MAX_DOCUMENTS}). \n'
                                 f'Используйте кнопку "{dictionary.CONTINUE}"')
            return

        documents.append(message.document.file_id)

        await state.update_data(documents=documents)

        keyboard = keyboards_general.continue_cancel_keyboard()
        await message.answer(f'Осталось свободных мест под документы: {MAX_DOCUMENTS - len(documents)}. \n'
                             f'Для перехода далее используйте кнопку "{dictionary.CONTINUE}"',
                             reply_markup=keyboard)

    async def create_text_admin(self, message: types.Message, state: FSMContext):
        text = message.text if message.text != dictionary.SKIP else None

        await state.update_data(text=text)
        await state.set_state(self.admins_states.CreateConfirm)

        data = await state.get_data()

        await message.answer(f'Название: {data["name"]}')

        media_group = MediaGroup()
        for document in data['documents']:
            media_group.attach_document(document)

        await message.answer_media_group(media_group)

        if data['text'] is not None:
            await message.answer(text=data['text'])

        keyboard = keyboards_general.confirm_keyboard()
        await message.answer('Вы действительно хотите создать данный шаблон?', reply_markup=keyboard)

    async def create_confirm_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        data = await state.get_data()
        data_db = {'documents': data['documents'], 'text': data['text']}
        await self.smg_bot.db.create_subcategory(self.name_button, path, data['name'], data_db)

        await message.answer('Успешно создан шаблон')
        await self.cancel_admin(message, state)

    def register_admin_events(self, dp: Dispatcher):
        super().register_admin_events(dp)

        dp.register_message_handler(self.create_name_admin, content_types=ContentType.TEXT,
                                    state=self.admins_states.CreateName)
        dp.register_message_handler(self.create_document_admin, is_media_group=False,
                                    content_types=ContentType.DOCUMENT, state=self.admins_states.CreateDocument)
        dp.register_message_handler(self.create_document_admin, Text(dictionary.CONTINUE),
                                    state=self.admins_states.CreateDocument)
        dp.register_message_handler(self.create_text_admin, content_types=ContentType.TEXT,
                                    state=self.admins_states.CreateText)
        dp.register_message_handler(self.create_confirm_admin, Text(dictionary.CONFIRM),
                                    state=self.admins_states.CreateConfirm)
