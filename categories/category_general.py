from email.mime.text import MIMEText

from aiogram.dispatcher import FSMContext

from states.states_admin import CategoryStatesAdmin


class Category:
    def __init__(self, smg_bot, name_button: str,
                 user_states, admin_states,
                 create_button: str = None, edit_button: str = None, delete_button: str = None,
                 msg_choice: str = None, with_subcategories: bool = True, subcategories_is_object: bool = True):

        from bot_main import SMGBot

        self.smg_bot: SMGBot = smg_bot

        self.name_button: str = name_button

        self.user_states = user_states
        self.admins_states: CategoryStatesAdmin = admin_states

        self.delete_button: str = delete_button
        self.edit_button: str = edit_button
        self.create_button: str = create_button

        self.msg_choice: str = msg_choice
        self.with_subcategories: bool = with_subcategories
        self.subcategories_is_object: bool = subcategories_is_object

    async def get_path(self, state: FSMContext):
        data = await state.get_data()

        return data.get('path', [])

    async def check_data_in_subcategories(self, path):
        subcategories = await self.smg_bot.db.get_subcategories(self.name_button, path)
        for subcategory in subcategories:
            if await self.smg_bot.db.get_data(self.name_button, path + [subcategory]):
                return True

        return False

    async def check_can_create_object(self, path):
        subcategories = await self.smg_bot.db.get_subcategories(self.name_button, path)
        for subcategory in subcategories:
            if not await self.smg_bot.db.get_data(self.name_button, path + [subcategory]):
                return False

        return True

    async def send_email_message(self, receiver, subject, message):
        msg = MIMEText(message)
        msg['Subject'] = subject

        self.smg_bot.server_email.sendmail(self.smg_bot.sender_email, receiver, msg.as_string())
