from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

import dictionary
from categories.categories import Contacts
from keyboards import keyboards_general
from states.states_admin import ContactsStatesAdmin


class ContactsAdmin(Contacts):
    def __init__(self, smg_bot):
        super().__init__(smg_bot)

        self.admins_states = ContactsStatesAdmin

    async def event_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)
        if not (data_db := await self.smg_bot.db.get_data(self.name_button, path)):
            return

        contacts = data_db['contacts']

        for contact in contacts:
            fio = f'{contact["surname"]} {contact["name"]} {contact["patronymic"]}'

            await message.answer_photo(photo=contact['photo'],
                                       caption=f'{fio}\n'
                                               f'{contact["job"]}\n'
                                               f'{contact["email"]}')
    ############################################################################################
    ############################################################################################
    async def create_object_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        if await self.smg_bot.db.get_subcategories(self.name_button, path):
            await message.answer('Нельзя добавить контакт, так где есть подкатегории')
            return

        await state.set_state(self.admins_states.CreateFIO)

        keyboard = keyboards_general.cancel_keyboard()
        await message.answer('Введите ФИО через пробел (Пример: Петров Петр Петрович)', reply_markup=keyboard)

    async def create_fio_admin(self, message: types.Message, state: FSMContext):
        if len(message.text.split(' ')) != 3:
            await message.answer('Неправильный формат ФИО (Пример: Петров Петр Петрович)')
            return

        surname, name, patronymic = message.text.title().split(' ')

        await state.update_data(surname=surname, name=name, patronymic=patronymic)
        await state.set_state(self.admins_states.CreateJob)

        await message.answer('Введите должность')

    async def create_job_admin(self, message: types.Message, state: FSMContext):
        job = message.text

        await state.update_data(job=job)
        await state.set_state(self.admins_states.CreateEmail)

        await message.answer('Введите электронную почту')

    async def create_email_admin(self, message: types.Message, state: FSMContext):
        email = message.text

        await state.update_data(email=email)
        await state.set_state(self.admins_states.CreatePhoto)

        await message.answer('Отправьте фотографию человека')

    async def create_photo_admin(self, message: types.Message, state: FSMContext):
        photo = message.photo[0].file_id

        await state.update_data(photo=photo)
        await state.set_state(self.admins_states.CreateConfirm)

        contact = await state.get_data()
        fio = f'{contact["surname"]} {contact["name"]} {contact["patronymic"]}'

        await message.answer_photo(photo=contact['photo'],
                                   caption=f'{fio}\n'
                                           f'{contact["job"]}\n'
                                           f'{contact["email"]}')

        keyboard = keyboards_general.confirm_cancel_keyboard()
        await message.answer('Вы действительно хотите создать данный контакт?', reply_markup=keyboard)

    async def create_confirm_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        data = await state.get_data()
        data_db = {'surname': data["surname"], 'name': data['name'], 'patronymic': data['patronymic'],
                   'job': data['job'], 'email': data['email'], 'photo': data['photo']}

        await self.smg_bot.db.add_data(self.name_button, path, 'contacts', data_db)
        await message.answer('Успешно создан контакт')

        await self.cancel_admin(message, state)

    ############################################################################################
    ############################################################################################

    def register_admin_events(self, dp: Dispatcher):
        super().register_admin_events(dp)
        dp.register_message_handler(self.create_fio_admin, content_types=ContentType.TEXT,
                                   state=self.admins_states.CreateFIO)
        dp.register_message_handler(self.create_job_admin, content_types=ContentType.TEXT,
                                    state=self.admins_states.CreateJob)
        dp.register_message_handler(self.create_email_admin, content_types=ContentType.TEXT,
                                    state=self.admins_states.CreateEmail)
        dp.register_message_handler(self.create_photo_admin, content_types=ContentType.PHOTO,
                                    state=self.admins_states.CreatePhoto)
        dp.register_message_handler(self.create_confirm_admin, Text(dictionary.CONFIRM),
                                    state=self.admins_states.CreateConfirm)

