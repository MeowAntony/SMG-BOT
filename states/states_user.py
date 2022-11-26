import pyclbr
import sys

from aiogram.dispatcher.filters.state import StatesGroup, State


class CategoryStatesUser(StatesGroup):
    ChooseCategory = State()
    Chosen = State()


class ContactsStatesUser(CategoryStatesUser):
    Chosen = State()


class FAQStatesUser(CategoryStatesUser):
    Chosen = State()

    QuestionSelected = State()


class LearningStatesUser(CategoryStatesUser):
    Chosen = State()


class TemplatesStatesUser(CategoryStatesUser):
    Chosen = State()


class RegulationsStatesUser(CategoryStatesUser):
    Chosen = State()
    DocumentSelected = State()


class LogsErrorsVictoriesStatesUser(CategoryStatesUser):
    Chosen = State()


class FeedbackStatesUser(CategoryStatesUser):
    Chosen = State()

    SendMessage = State()
    SendConfirm = State()


class ITRequestsStatesUser(CategoryStatesUser):
    Chosen = State()

    SendMessage = State()
    SendConfirm = State()


class HRRequestsStatesUser(CategoryStatesUser):
    Message = State()
    Confirm = State()


class AboutBotStatesUser(CategoryStatesUser):
    Chosen = State()
    pass


ALL_CLASSES = [CategoryStatesUser, ContactsStatesUser, LearningStatesUser, TemplatesStatesUser, RegulationsStatesUser,
               LogsErrorsVictoriesStatesUser, FeedbackStatesUser, ITRequestsStatesUser, AboutBotStatesUser]
ALL_USER_STATES = []

for class_ in ALL_CLASSES:
    ALL_USER_STATES += class_.states
