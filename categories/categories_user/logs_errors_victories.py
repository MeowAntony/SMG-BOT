from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from categories.categories import LogsErrorsVictories


class LogsErrorsVictoriesUser(LogsErrorsVictories):
    def __init__(self, smg_bot):
        super().__init__(smg_bot)

    async def event_user(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state) + [message.text]

        if not (data_db := await self.smg_bot.db.get_data(self.name_button, path)):
            return

        text = data_db['text']

        await message.answer(text=text)

    def register_events(self, dp: Dispatcher):
        # dp.register_message_handler(self.subcategory_handler, state=ContactsStates.ChooseSubcategory)
        pass
