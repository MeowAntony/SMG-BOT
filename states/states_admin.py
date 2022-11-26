from aiogram.dispatcher.filters.state import StatesGroup, State


class CategoryStatesAdmin(StatesGroup):
    ChooseCategory = State()
    Chosen = State()

    CreateSubcategory = State()
    CreateConfirm = State()

    EditOldName = State()
    EditNewName = State()
    EditConfirm = State()

    DeleteSubcategory = State()
    DeleteConfirm = State()


class ContactsStatesAdmin(CategoryStatesAdmin):
    Chosen = State()

    CreateFIO = State()
    CreateJob = State()
    CreateEmail = State()
    CreatePhoto = State()
    CreateConfirm = State()

    # EditDescription = State()
    # EditConfirm = State()


class FAQStatesAdmin(CategoryStatesAdmin):
    Chosen = State()

    CreateName = State()
    CreateAnswer = State()
    CreatePath = State()
    CreateConfirm = State()


class LearningStatesAdmin(CategoryStatesAdmin):
    Chosen = State()

    CreateName = State()
    CreateVideo = State()
    CreateURL = State()
    CreateConfirm = State()
    # EditDescription = State()
    # EditConfirm = State()


class TemplatesStatesAdmin(CategoryStatesAdmin):
    Chosen = State()

    CreateName = State()
    CreateDocument = State()
    CreateText = State()
    CreateConfirm = State()


class RegulationsStatesAdmin(CategoryStatesAdmin):
    Chosen = State()

    CreateName = State()
    CreateDocument = State()
    CreateConfirm = State()


class LogsErrorsVictoriesStatesAdmin(CategoryStatesAdmin):
    Chosen = State()

    CreateName = State()
    CreateText = State()
    CreateConfirm = State()


class FeedbackStatesAdmin(CategoryStatesAdmin):
    Chosen = State()

    EditInfo = State()
    EditConfirm = State()


class ITRequestsStatesAdmin(CategoryStatesAdmin):
    Chosen = State()

    EditInfo = State()
    EditEmail = State()
    # EditMessageToEmail = State() TODO
    EditInfoConfirm = State()


class AboutBotStatesAdmin(CategoryStatesAdmin):
    Chosen = State()

    EditDescription = State()
    EditConfirm = State()


ALL_CLASSES = [ContactsStatesAdmin, LearningStatesAdmin, TemplatesStatesAdmin, RegulationsStatesAdmin,
               LogsErrorsVictoriesStatesAdmin, FeedbackStatesAdmin, ITRequestsStatesAdmin, AboutBotStatesAdmin]
ALL_ADMIN_STATES = set()

for class_ in ALL_CLASSES:
    for state in class_.states:
        ALL_ADMIN_STATES.add(state)

ALL_ADMIN_STATES = list(ALL_ADMIN_STATES)
