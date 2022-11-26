from aiogram import types
from aiogram.dispatcher import FSMContext

from categories.categories import AboutBot


class AboutBotUser(AboutBot):
    def __init__(self, smg_bot):
        super().__init__(smg_bot)

    async def event_user(self, message: types.Message, state: FSMContext):
        if not (data_db := await self.smg_bot.db.get_data(self.name_button)):
            return

        text = data_db['description']
        await message.answer(text)
