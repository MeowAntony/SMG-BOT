from .category_admin import CategoryAdmin
from .category_user import CategoryUser
from states.states_admin import AboutBotStatesAdmin, ContactsStatesAdmin, LearningStatesAdmin, RegulationsStatesAdmin, \
    LogsErrorsVictoriesStatesAdmin, TemplatesStatesAdmin, FeedbackStatesAdmin, ITRequestsStatesAdmin, FAQStatesAdmin
from states.states_user import AboutBotStatesUser, ContactsStatesUser, LearningStatesUser, RegulationsStatesUser, \
    LogsErrorsVictoriesStatesUser, TemplatesStatesUser, FeedbackStatesUser, ITRequestsStatesUser, FAQStatesUser


class Contacts(CategoryUser, CategoryAdmin):
    def __init__(self, smg_bot):
        super().__init__(smg_bot=smg_bot, name_button='Контакты', user_states=ContactsStatesUser,
                         admin_states=ContactsStatesAdmin, create_button='Добавить контакт',
                         edit_button='Изменить контакт', delete_button='Удалить контакт', msg_choice='Выберите контакт',
                         subcategories_is_object=False)


class FAQ(CategoryUser, CategoryAdmin):
    def __init__(self, smg_bot):
        super().__init__(smg_bot=smg_bot, name_button='FAQ',
                         user_states=FAQStatesUser, admin_states=FAQStatesAdmin,
                         msg_choice='Выберите вопрос',
                         create_button='Создать вопрос', edit_button='Изменить вопрос', delete_button='Удалить вопрос')


class Learning(CategoryUser, CategoryAdmin):
    def __init__(self, smg_bot):
        super().__init__(smg_bot=smg_bot, name_button='Обучение', user_states=LearningStatesUser,
                         admin_states=LearningStatesAdmin, msg_choice='Выберите обучение',
                         create_button='Создать обучение', edit_button='Изменить обучение',
                         delete_button='Удалить обучение')


class Templates(CategoryUser, CategoryAdmin):
    def __init__(self, smg_bot):
        super().__init__(smg_bot=smg_bot, name_button='Шаблоны проектных документов',
                         user_states=TemplatesStatesUser, admin_states=TemplatesStatesAdmin,
                         msg_choice='Выберите шаблон', create_button='Создать шаблон', edit_button='Изменить шаблон',
                         delete_button='Удалить шаблон')


class Regulations(CategoryUser, CategoryAdmin):
    def __init__(self, smg_bot):
        super().__init__(smg_bot=smg_bot, name_button='Нормативные документы',
                         user_states=RegulationsStatesUser, admin_states=RegulationsStatesAdmin,
                         msg_choice='Выберите документ', create_button='Создать документ',
                         edit_button='Изменить документ', delete_button='Удалить документ')


class LogsErrorsVictories(CategoryUser, CategoryAdmin):
    def __init__(self, smg_bot):
        super().__init__(smg_bot=smg_bot, name_button='Журнал ошибок и побед',
                         user_states=LogsErrorsVictoriesStatesUser, admin_states=LogsErrorsVictoriesStatesAdmin,
                         msg_choice='Выберите журнал', create_button='Создать журнал', edit_button='Изменить журнал',
                         delete_button='Удалить журнал')


class Feedback(CategoryUser, CategoryAdmin):
    def __init__(self, smg_bot):
        super().__init__(smg_bot=smg_bot, name_button='Обратная связь',
                         user_states=FeedbackStatesUser, admin_states=FeedbackStatesAdmin,
                         edit_button='Изменить сообщение', with_subcategories=False)


class ITRequests(CategoryUser, CategoryAdmin):
    def __init__(self, smg_bot):
        super().__init__(smg_bot=smg_bot, name_button='Заявки в IT',
                         user_states=ITRequestsStatesUser, admin_states=ITRequestsStatesAdmin,
                         edit_button='Изменить сообщение', with_subcategories=False)


class HRRequests(CategoryUser, CategoryAdmin):
    def __init__(self, smg_bot, is_admin):
        super().__init__(smg_bot=smg_bot, is_admin=is_admin, name_button='Обратная связь',
                         edit_button='Изменить сообщение', with_subcategories=False)


class AboutBot(CategoryUser, CategoryAdmin):
    def __init__(self, smg_bot):
        super().__init__(smg_bot=smg_bot, name_button='О Боте',
                         user_states=AboutBotStatesUser, admin_states=AboutBotStatesAdmin,
                         edit_button='Изменить описание', with_subcategories=False)
