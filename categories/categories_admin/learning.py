from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

from categories.categories import Learning
import dictionary
from keyboards import keyboards_general
from states.states_admin import LearningStatesAdmin


class LearningAdmin(Learning):
    def __init__(self, smg_bot):
        super().__init__(smg_bot)
        self.admins_states = LearningStatesAdmin

    async def event_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state) + [message.text]

        if not (data_db := await self.smg_bot.db.get_data(self.name_button, path)):
            return

        video, url = data_db['video'], data_db['url']
        if video is not None:
            await message.answer_video(video=video)
        if url is not None:
            await message.answer(text=url)

    async def create_object_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        if not await self.check_can_create_object(path):
            await message.answer('Нельзя добавить видео-обучение, так где есть подкатегории')
            return

        await state.set_state(self.admins_states.CreateName)

        keyboard = keyboards_general.cancel_keyboard()
        await message.answer('Введите название обучения', reply_markup=keyboard)

    async def create_name_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        name = message.text

        if name in await self.smg_bot.db.get_subcategories(self.name_button, path):
            await message.answer('Введенное название уже существует в текущей подкатегории')
            return

        await state.update_data(name=name)
        await state.set_state(self.admins_states.CreateVideo)

        keyboard = keyboards_general.skip_cancel_keyboard()
        await message.answer('Прикрепите видео (видео, а не файл) или пропустите данный пункт', reply_markup=keyboard)

    async def create_video_admin(self, message: types.Message, state: FSMContext):
        video = message.video.file_id if message.text != dictionary.SKIP else None

        await state.update_data(video=video)

        await state.set_state(self.admins_states.CreateURL)

        await message.answer('Введите ссылку на видео')

    async def create_url_admin(self, message: types.Message, state: FSMContext):
        url = message.text if message.text != dictionary.SKIP else None

        await state.update_data(url=url)

        await state.set_state(self.admins_states.CreateConfirm)

        data = await state.get_data()

        if data['video'] is None and data['url'] is None:
            await message.answer('Ничего не добавлено')
            await self.cancel_admin(message, state)
            return

        await message.answer(f'Название: {data["name"]}')

        if data["video"] is not None:
            await message.answer_video(video=data["video"])
        if data["url"] is None:
            await message.answer(text=data["url"])

        keyboard = keyboards_general.confirm_keyboard()
        await message.answer('Вы действительно хотите создать данное обучение?', reply_markup=keyboard)

    async def create_confirm_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        data = await state.get_data()
        data_db = {'video': data['video'], 'url': data['url']}
        await self.smg_bot.db.create_subcategory(self.name_button, path, data['name'], data_db)

        await message.answer('Успешно создано обучение')
        await self.cancel_admin(message, state)

    def register_admin_events(self, dp: Dispatcher):
        super().register_admin_events(dp)

        dp.register_message_handler(self.create_name_admin, content_types=ContentType.TEXT,
                                    state=self.admins_states.CreateName)
        dp.register_message_handler(self.create_video_admin, content_types=ContentType.VIDEO,
                                    state=self.admins_states.CreateVideo)
        dp.register_message_handler(self.create_video_admin, Text(dictionary.SKIP),
                                    state=self.admins_states.CreateVideo)
        dp.register_message_handler(self.create_url_admin, content_types=ContentType.TEXT,
                                    state=self.admins_states.CreateURL)
        dp.register_message_handler(self.create_confirm_admin, Text('Подтвердить'),
                                    state=self.admins_states.CreateConfirm)
