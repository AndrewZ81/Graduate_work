from django.core.management.base import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import Message
from goals.models import Goal, Status, GoalCategory


class Command(BaseCommand):
    """
    Описывает команду 'manage.py runbot'
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()
        self.offset: int = 0

    def handle(self, *args, **options):
        """
        Конструирует общую логику работы команды
        """
        while True:
            response = self.tg_client.get_updates(offset=self.offset)
            for item in response.result:
                self.offset = item.update_id + 1
                self.handle_authorization(item.message)

    def handle_authorization(self, msg: Message):
        """
        Конструирует логику проверки состояния авторизации пользователя Telegram
        в Веб-приложении TodoList
        """
        tg_user, created = TgUser.objects.get_or_create(chat_id=msg.chat.id)

        if not tg_user.user:
            self.handle_unauthorized_user(tg_user, msg)
        else:
            self.handle_authorized_user(tg_user, msg)

    def handle_unauthorized_user(self, tg_user: TgUser, msg: Message):
        """
        Конструирует логику работы с неавторизованным пользователем
        """
        code = tg_user.set_verification_code()
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f"Здравствуйте. Чтобы я Вас узнал, авторизуйтесь на сайте andrewzaiko.ga.\n"
                 f"После этого используйте код верификации бота, приведенный ниже.\n"
                 f"Ваш код верификации: {code}"
        )

    def handle_authorized_user(self, tg_user: TgUser, msg: Message):
        """
        Конструирует логику работы с авторизованным пользователем
        """
        if msg.text == "/goals":
            self.handle_goals(tg_user, msg)
        elif msg.text == "/create":
            self.handle_create(tg_user, msg)
        elif msg.text == "/cancel":
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text="Используйте эту команду только в режиме создания целей"
            )
        else:
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text="Неизвестная команда. Для просмотра списка команд наберите /"
            )

    def handle_goals(self, tg_user: TgUser, msg: Message):
        """
        Конструирует логику отображения всех активных целей пользователя
        """
        goals_as_objects = Goal.objects.filter(
            category__board__participants__user_id=tg_user.user_id,
            category__is_deleted=False
        ).exclude(status=Status.archived)

        goals_as_str: str = "\n".join([goal.title for goal in goals_as_objects])

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f"Ваши цели:\n\n{goals_as_str}"
        )

    def handle_create(self, tg_user: TgUser, msg: Message):
        """
        Конструирует логику создания цели пользователя
        """
        categories_as_objects = GoalCategory.objects.filter(
            board__participants__user_id=tg_user.user_id,
            is_deleted=False
        )
        categories_as_str: str = "\n".join(
            [category.title for category in categories_as_objects]
        )
        categories_as_dict: dict = {
            category.title: category for category in categories_as_objects
        }

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f"Выберите категорию из приведенных ниже:\n\n"
                 f"{categories_as_str}\n\n"
                 f"Для отмены введите /cancel"
        )

        flag = True
        while flag:
            response = self.tg_client.get_updates(offset=self.offset)
            for item in response.result:
                self.offset = item.update_id + 1
                if item.message.text in categories_as_dict:
                    category = categories_as_dict.get(item.message.text)
                    self.create_goal(tg_user, msg, category)
                    flag = False
                elif item.message.text == '/cancel':
                    self.tg_client.send_message(
                        chat_id=msg.chat.id, text="Создание цели отменено"
                    )
                    flag = False
                else:
                    self.tg_client.send_message(
                        chat_id=msg.chat.id,
                        text=f"Категория '{item.message.text}' не существует!"
                    )

    def create_goal(self, tg_user: TgUser, msg: Message, category: GoalCategory):
        """
        Создаёт новую цель пользователя
        """
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f"Введите заголовок для цели\n"
                 f"Для отмены введите /cancel"
        )
        flag = True
        while flag:
            response = self.tg_client.get_updates(offset=self.offset)
            for item in response.result:
                self.offset = item.update_id + 1
                if item.message.text == '/cancel':
                    self.tg_client.send_message(
                        chat_id=msg.chat.id, text="Создание цели отменено"
                    )
                else:
                    goal = Goal.objects.create(
                        title=item.message.text,
                        category_id=category.id,
                        user_id=tg_user.user_id
                    )
                    self.tg_client.send_message(
                        chat_id=msg.chat.id,
                        text=f"Цель '{item.message.text}' создана. Вот ссылка на неё:\n"
                             f"http://127.0.0.1/boards/{category.board.id}/"
                             f"categories/{category.id}/goals?goal={goal.id}"
                    )
                flag = False
