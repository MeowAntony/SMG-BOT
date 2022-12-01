from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

import dictionary
from categories.categories import Contacts
from keyboards import keyboards_general, keyboards_admin
from states.states_admin import ContactsStatesAdmin


class ContactsAdmin(Contacts):
    def __init__(self, smg_bot):
        super().__init__(smg_bot)

        self.admins_states = ContactsStatesAdmin

    async def event_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)
        if not (data_db := await self.smg_bot.db.get_data(self.name_button, path)):
            return

        contacts = data_db.get('contacts', [])

        for contact in contacts:
            photo = contact['photo']
            caption = f'{contact["fio"]} \n' \
                      f'{contact["job"]} \n' \
                      f'{contact["email"]}'

            await message.answer_photo(photo=photo, caption=caption)

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

        fio = message.text.title()

        path = await self.get_path(state)

        data_db = await self.smg_bot.db.get_data(self.name_button, path)
        contacts = data_db.get('contacts', [])
        people = [person['fio'] for person in contacts]

        if fio in people:
            await message.answer('Данная персона уже создана')
            return

        await state.update_data(fio=fio)
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

        await message.answer_photo(photo=contact['photo'],
                                   caption=f'{contact["fio"]}\n'
                                           f'{contact["job"]}\n'
                                           f'{contact["email"]}')

        keyboard = keyboards_general.confirm_cancel_keyboard()
        await message.answer('Вы действительно хотите создать данный контакт?', reply_markup=keyboard)

    async def create_confirm_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        data = await state.get_data()
        data_db = {'fio': data['fio'], 'job': data['job'],
                   'email': data['email'], 'photo': data['photo']}

        await self.smg_bot.db.add_data(self.name_button, path, 'contacts', data_db)
        await message.answer('Успешно создан контакт')

        await self.cancel_admin(message, state)

    ############################################################################################
    ############################################################################################

    async def edit_object_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        data_db = await self.smg_bot.db.get_data(self.name_button, path)

        contacts = data_db.get('contacts', [])
        people = [person["fio"] for person in contacts]

        await state.set_state(self.admins_states.EditSelectPerson)

        keyboard = keyboards_general.cancel_keyboard()
        keyboard = keyboards_admin.with_subcategories_keyboard(keyboard, people)
        await message.answer('Выберите ФИО персоны, которую хотите изменить', reply_markup=keyboard)

    async def edit_select_person_admin(self, message: types.Message, state: FSMContext):
        fio_old = message.text.title()

        path = await self.get_path(state)

        data_db = await self.smg_bot.db.get_data(self.name_button, path)
        contacts = data_db.get('contacts', [])
        people = {person["fio"]: person for person in contacts}

        if fio_old not in people:
            await message.answer('Данная персона не найдена')
            return

        old_person = people[fio_old]
        await state.update_data(fio_old=fio_old, fio=old_person['fio'],
                                job=old_person['job'], email=old_person['email'], photo=old_person['photo'])
        await state.set_state(self.admins_states.EditFIO)

        keyboard = keyboards_general.skip_cancel_keyboard()
        await message.answer(f'Текущее ФИО: {fio_old} \n\n'
                             'Введите новые ФИО через пробел (Пример: Петров Петр Петрович) или пропустите',
                             reply_markup=keyboard)

    async def edit_fio_admin(self, message: types.Message, state: FSMContext):
        if message.text != dictionary.SKIP:
            if len(message.text.split(' ')) != 3:
                await message.answer('Неправильный формат ФИО (Пример: Петров Петр Петрович)')
                return

            path = await self.get_path(state)

            data_db = await self.smg_bot.db.get_data(self.name_button, path)
            contacts = data_db.get('contacts', [])
            people = [person["fio"] for person in contacts]

            new_fio = message.text.title()
            if new_fio in people:
                await message.answer('Данная персона уже создана')
                return

            await state.update_data(fio=new_fio)

        await state.set_state(self.admins_states.EditJob)

        data = await state.get_data()

        await message.answer(f'Текущая должность: {data["job"]} \n\n'
                             f'Введите новую должность или пропустите')

    async def edit_job_admin(self, message: types.Message, state: FSMContext):
        if message.text != dictionary.SKIP:
            job = message.text
            await state.update_data(job=job)

        await state.set_state(self.admins_states.EditEmail)

        data = await state.get_data()

        await message.answer(f'Текущая электронная почта: {data["email"]} \n\n'
                             f'Введите новую электронную почту или пропустите')

    async def edit_email_admin(self, message: types.Message, state: FSMContext):
        if message.text != dictionary.SKIP:
            email = message.text
            await state.update_data(email=email)

        await state.set_state(self.admins_states.EditPhoto)

        data = await state.get_data()

        await message.answer_photo(photo=data["photo"], caption='Текущая фотография')
        await message.answer(f'Отправьте новую фотографию человека или пропустите')

    async def edit_photo_admin(self, message: types.Message, state: FSMContext):
        if message.text != dictionary.SKIP:
            photo = message.photo[0].file_id
            await state.update_data(photo=photo)

        contact = await state.get_data()

        photo = contact['photo']
        caption = f'{contact["fio"]} \n' \
                  f'{contact["job"]} \n' \
                  f'{contact["email"]}'

        await state.set_state(self.admins_states.EditConfirm)
        await state.update_data(contact=contact)

        await message.answer_photo(photo=photo, caption=caption)

        keyboard = keyboards_general.confirm_cancel_keyboard()
        await message.answer('Вы действительно хотите изменить старый контакт на этот новый?', reply_markup=keyboard)

    async def edit_confirm_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        contact = await state.get_data()
        data_db = {'fio': contact['fio'], 'job': contact['job'],
                   'email': contact['email'], 'photo': contact['photo']}

        await self.smg_bot.db.edit_contact(self.name_button, path, contact['fio_old'], data_db)

        await message.answer('Успешно изменён контакт')

        await self.cancel_admin(message, state)

    ############################################################################################
    ############################################################################################

    async def delete_object_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        data_db = await self.smg_bot.db.get_data(self.name_button, path)

        contacts = data_db.get('contacts', [])
        people = [person["fio"] for person in contacts]

        await state.set_state(self.admins_states.DeleteSelectPerson)

        keyboard = keyboards_general.cancel_keyboard()
        keyboard = keyboards_admin.with_subcategories_keyboard(keyboard, people)
        await message.answer('Выберите ФИО персоны, которую хотите удалить', reply_markup=keyboard)

    async def delete_select_person_admin(self, message: types.Message, state: FSMContext):
        fio = message.text.title()

        path = await self.get_path(state)

        data_db = await self.smg_bot.db.get_data(self.name_button, path)
        contacts = data_db.get('contacts', [])
        people = {person["fio"]: person for person in contacts}

        if fio not in people:
            await message.answer('Данная персона не найдена')
            return

        await state.update_data(fio=fio)
        await state.set_state(self.admins_states.DeleteConfirm)

        contact = people[fio]

        photo = contact['photo']
        caption = f'{contact["fio"]} \n' \
                  f'{contact["job"]} \n' \
                  f'{contact["email"]}'

        await message.answer_photo(photo=photo, caption=caption)

        keyboard = keyboards_general.confirm_cancel_keyboard()
        await message.answer(f'Вы действительно хотите удалить этот контакт?',
                             reply_markup=keyboard)

    async def delete_confirm_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        data = await state.get_data()

        await self.smg_bot.db.delete_contact(self.name_button, path, data['fio'])

        await message.answer('Успешно удалён контакт')

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

        dp.register_message_handler(self.edit_select_person_admin, content_types=ContentType.TEXT,
                                    state=self.admins_states.EditSelectPerson)
        dp.register_message_handler(self.edit_fio_admin, content_types=ContentType.TEXT,
                                    state=self.admins_states.EditFIO)
        dp.register_message_handler(self.edit_job_admin, content_types=ContentType.TEXT,
                                    state=self.admins_states.EditJob)
        dp.register_message_handler(self.edit_email_admin, content_types=ContentType.TEXT,
                                    state=self.admins_states.EditEmail)
        dp.register_message_handler(self.edit_photo_admin, content_types=ContentType.PHOTO,
                                    state=self.admins_states.EditPhoto)
        dp.register_message_handler(self.edit_photo_admin, Text(dictionary.SKIP),
                                    state=self.admins_states.EditPhoto)
        dp.register_message_handler(self.edit_confirm_admin, Text(dictionary.CONFIRM),
                                    state=self.admins_states.EditConfirm)

        dp.register_message_handler(self.delete_select_person_admin, content_types=ContentType.TEXT,
                                    state=self.admins_states.DeleteSelectPerson)
        dp.register_message_handler(self.delete_confirm_admin, Text(dictionary.CONFIRM),
                                    state=self.admins_states.DeleteConfirm)
