import logging
import smtplib

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.types import MediaGroup

import config
from categories.categories_admin import *
from categories.categories_admin.faq import FAQAdmin
from categories.categories_admin.feedback import FeedbackAdmin
from categories.categories_admin.logs_errors_victories import LogsErrorsVictoriesAdmin
from categories.categories_admin.templates import TemplatesAdmin
from categories.categories_user.about_bot import AboutBotUser
from categories.categories_user.contacts import ContactsUser
from categories.categories_user.faq import FAQUser
from categories.categories_user.feedback import FeedbackUser
from categories.categories_user.it_requests import ITRequestsUser
from categories.categories_user.learning import LearningUser
from categories.categories_user.logs_errors_victories import LogsErrorsVictoriesUser
from categories.categories_user.regulations import RegulationsUser
from categories.categories_user.templates import TemplatesUser
from dbmanager import DataBaseManager
from handlers.handler_admin import AdminHandler
from handlers.handler_user import UserHandler


class SMGBot:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

        self._load_categories()
        # self._init_email()

        self.bot = Bot(config.TOKEN)
        self._storage = MongoStorage(db_name=config.MONGO_DB_NAME)
        self.dp = Dispatcher(self.bot, storage=self._storage)

        self.db: DataBaseManager = DataBaseManager()

        self.handler_user = UserHandler(self.db, self._categories_user)
        self.handler_admin = AdminHandler(self.db, self._categories_admin)
        # self._add_categories_to_db() TODO сделать

        self._event_handler()

    def _load_categories(self):  # TODO сделать, чтобы автоматически

        categories_user_list = [ContactsUser(self), FAQUser(self), LearningUser(self), TemplatesUser(self),
                                RegulationsUser(self), LogsErrorsVictoriesUser(self), FeedbackUser(self),
                                AboutBotUser(self)]
        self._categories_user = {category.name_button: category for category in categories_user_list}

        categories_admin_list = [ContactsAdmin(self), FAQAdmin(self), LearningAdmin(self), TemplatesAdmin(self),
                                 RegulationsAdmin(self), LogsErrorsVictoriesAdmin(self), FeedbackAdmin(self),
                                 AboutBotAdmin(self)]
        self._categories_admin = {category.name_button: category for category in categories_admin_list}

    def _add_categories_to_db(self):
        # TODO сделать, чтобы категории загружались при запуске

        """for category in self._categories:
            print(self.db.check_category(category.name_db).__dict__)
            if not self.db.check_category(category.name_db):
                self.db.create_category(category.name_db)"""

    def _init_email(self):
        # TODO сделать почту
        self.sender_email = config.EMAIL_LOGIN
        print(0)
        self.server_email = smtplib.SMTP_SSL(config.EMAIL_SERVER, config.EMAIL_PORT)
        print(2)
        self.server_email.login(self.sender_email, config.EMAIL_PASSWORD)
        print(3)

    def _event_handler(self):
        @self.dp.message_handler(is_media_group=True, content_types=types.ContentType.ANY, state='*')
        async def msg_handler_keyboard(message: types.Message):
            print(message.media_group_id)
            media = MediaGroup()
            media.attach_document(message.document.file_id, caption='123')

            print(message)
            await message.answer_media_group(media)

        self.handler_user.register_user_command_events(self.dp)
        self.handler_admin.register_admin_command_events(self.dp)
        self.handler_user.register_user_events(self.dp)
        self.handler_admin.register_admin_events(self.dp)

        # for category in self._categories:
        #    category.register_events(self.dp)

        executor.start_polling(self.dp, skip_updates=True, on_shutdown=self._shutdown)

    async def _shutdown(self, dp: Dispatcher):
        await dp.storage.close()
        await dp.storage.wait_closed()

        self.server_email.close()


if __name__ == '__main__':
    SMGBot()
