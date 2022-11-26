from typing import List

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from categories.category_general import Category
from keyboards import keyboards_admin


class CategoryAdmin(Category):
    def __init__(self, smg_bot, name_button: str, user_states, admin_states,
                 create_button: str = None, edit_button: str = None, delete_button: str = None,
                 msg_choice: str = None, with_subcategories: bool = True, subcategories_is_object: bool = True):
        super().__init__(smg_bot, name_button, user_states, admin_states, create_button, edit_button, delete_button,
                         msg_choice, with_subcategories, subcategories_is_object)

    async def select_category_admin(self, message: types.Message, state: FSMContext):
        await self.move_admin(message, state, [])

    async def subcategories_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        subcategory_next = message.text

        if subcategory_next not in await self.smg_bot.db.get_subcategories(self.name_button, path):
            await message.answer('Такого подкаталога не существует')
            return

        path.append(message.text)

        await self.move_admin(message, state, path)

    async def cancel_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        await state.reset_data()

        await self.move_admin(message, state, path)

    async def back_admin(self, message: types.Message, state: FSMContext):
        path = await self.get_path(state)

        if len(path) == 0:
            await self.smg_bot.handler_admin.main_menu(message, state)
            return

        path.pop(-1)

        await state.reset_data()

        await self.move_admin(message, state, path)

    async def move_admin(self, message: types.Message, state: FSMContext, path: List[str]):
        await state.set_state(self.admins_states.Chosen)

        if self.with_subcategories and not await self.smg_bot.db.get_data(self.name_button, path):
            subcategories = await self.smg_bot.db.get_subcategories(self.name_button, path)

            if not subcategories:
                keyboard = keyboards_admin.create_object_subcategory_keyboard(create_button=self.create_button,
                                                                              path=path)
            elif self.subcategories_is_object:
                if await self.check_data_in_subcategories(path):
                    keyboard = self.get_action_object_keyboard(path)
                    keyboard = keyboards_admin.action_object_subcategories_keyboard(keyboard, subcategories)
                else:
                    keyboard = keyboards_admin.action_subcategory_keyboard(subcategories, path)
            else:
                keyboard = keyboards_admin.action_subcategory_keyboard(subcategories, path)

            await state.update_data(category=self.name_button, path=path)

            await message.answer('Выберите действие', reply_markup=keyboard)
        else:
            if not self.subcategories_is_object or not self.with_subcategories:
                await state.update_data(category=self.name_button, path=path)

            await self.event_admin(message, state)

            if not self.subcategories_is_object or not self.with_subcategories:
                keyboard = self.get_action_object_keyboard(path)
                await message.answer('Выберите действие', reply_markup=keyboard)

    async def event_admin(self, message: types.Message, state: FSMContext):
        pass

    async def create_object_admin(self, message: types.Message, state: FSMContext):
        pass

    async def edit_object_admin(self, message: types.Message, state: FSMContext):
        pass

    async def delete_object_admin(self, message: types.Message, state: FSMContext):
        pass

    def register_action_objects(self, dp: Dispatcher):
        if self.create_button is not None:
            dp.register_message_handler(self.create_object_admin, Text(self.create_button),
                                        state=self.admins_states.Chosen)
        if self.edit_button is not None:
            dp.register_message_handler(self.edit_object_admin, Text(self.edit_button),
                                        state=self.admins_states.Chosen)
        if self.delete_button is not None:
            dp.register_message_handler(self.delete_object_admin, Text(self.delete_button),
                                        state=self.admins_states.Chosen)

    def get_action_object_keyboard(self, path: List[str] = None):
        return keyboards_admin.get_action_object_keyboard(create_button=self.create_button,
                                                          edit_button=self.edit_button,
                                                          delete_button=self.delete_button,
                                                          path=path)

    ##################################################################
    ##################################################################

    async def create_subcategory_admin(self, message: types.Message, state: FSMContext):
        await self.smg_bot.handler_admin.create_subcategory_admin(message, state)



    async def edit_subcategory_admin(self, message: types.Message, state: FSMContext):
        pass

    async def delete_subcategory_admin(self, message: types.Message, state: FSMContext):
        pass

    def register_action_subcategories(self, dp: Dispatcher):
        dp.register_message_handler(self.create_subcategory_admin, Text('Создать подкаталог'),
                                    state=self.admins_states.Chosen)


        dp.register_message_handler(self.edit_object_admin, Text('Изменить подкаталог'),
                                    state=self.admins_states.Chosen)
        dp.register_message_handler(self.delete_subcategory_admin, Text('Удалить подкаталог'),
                                    state=self.admins_states.Chosen)

    ##################################################################
    ##################################################################
    def register_admin_events(self, dp: Dispatcher):
        dp.register_message_handler(self.smg_bot.handler_admin.main_menu, Text('Главное меню'),
                                    state=self.admins_states)
        dp.register_message_handler(self.back_admin, Text('Назад'), state=self.admins_states)

        dp.register_message_handler(self.cancel_admin, Text('Отмена'), state=self.admins_states)
        self.register_action_objects(dp)
        self.register_action_subcategories(dp)

        dp.register_message_handler(self.select_category_admin, Text(self.name_button),
                                    state=self.admins_states.ChooseCategory)

        dp.register_message_handler(self.subcategories_admin, state=self.admins_states.Chosen)
        pass
