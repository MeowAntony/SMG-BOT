from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from categories.categories import HRRequests


class HRRequestsUser(HRRequests):
    def __init__(self, smg_bot):
        super().__init__(smg_bot)

    #TODO сделать
    async def event_user(self, message: types.Message, state: FSMContext):
        #if not (data_db := await self.antony_bot.db.get_data(self.name_db)):
        #    return

        text = "Напишите в одном сообщение заявку в HR. Она будет отправлена на почту."

        await state.set_state(UserHRRequestsStates.Message.state)

        keyboard = await self.antony_bot.keyboards_user.main_menu_keyboard()
        await message.answer(text=text, reply_markup=keyboard)

    async def send_message_to_email(self, message: types.Message, state: FSMContext):
        # TODO отправка на почту

        await state.set_state(UserChooseStates.ChooseCategory)

        keyboard = await self.antony_bot.keyboards_user.start_keyboard()
        await message.answer('Ваша заявка успешно отправлена!', reply_markup=keyboard)

    def register_events(self, dp: Dispatcher):
        dp.register_message_handler(self.send_message_to_email, content_types=['text'],
                                    state=UserHRRequestsStates.Message)
        pass
