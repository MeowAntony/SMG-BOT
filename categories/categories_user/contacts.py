from aiogram import types
from aiogram.dispatcher import FSMContext

from categories.categories import Contacts


class ContactsUser(Contacts):
    def __init__(self, smg_bot):
        super().__init__(smg_bot)

    async def event_user(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state) + [message.text]

        if not (data_db := await self.smg_bot.db.get_data(self.name_button, path)):
            return

        contacts = data_db['contacts']

        for contact in contacts:
            await message.answer_photo(photo=contact['photo'],
                                       caption=f'{contact["fio"]}\n'
                                               f'{contact["job"]}\n'
                                               f'{contact["email"]}')
