from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import MediaGroup

from categories.categories import Templates


class TemplatesUser(Templates):
    def __init__(self, smg_bot):
        super().__init__(smg_bot)

    async def event_user(self, message: types.Message, state: FSMContext):
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


