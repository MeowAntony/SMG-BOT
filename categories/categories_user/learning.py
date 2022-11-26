from aiogram import types
from aiogram.dispatcher import FSMContext

from categories.categories import Learning


class LearningUser(Learning):
    def __init__(self, smg_bot):
        super().__init__(smg_bot)

    async def event_user(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state) + [message.text]

        if not (data_db := await self.smg_bot.db.get_data(self.name_button, path)):
            return

        video, url = data_db['video'], data_db['url']
        if video:
            await message.answer_video(video=video)
        if url:
            await message.answer(text=url)

        await self.back_user(message, state)
