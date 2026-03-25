from tortoise import Tortoise
import os
import logging
from .Models import User, BotUser


logger = logging.getLogger(__name__)


async def init():
    """
    Порядок:
    1. DATABASE_URL (если задана)
    2. Конструктор из POSTGRES_* переменных
    3. Fallback sqlite (для локального запуска без настроек)
    """
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        db_url = db_url.strip()
    if not db_url:
        user = os.getenv("POSTGRES_USER", "").strip()
        password = os.getenv("POSTGRES_PASSWORD", "").strip()
        host = os.getenv("POSTGRES_HOST", "").strip()
        port = os.getenv("POSTGRES_PORT", "5432").strip()
        name = os.getenv("POSTGRES_DB", "").strip()
        if not port.isdigit():

            port = "5432"
        if user and password and host and name:
            db_url = f"postgres://{user}:{password}@{host}:{port}/{name}"
    if not db_url:

        db_url = "sqlite://db.sqlite3"
    logger.info(f"Инициализация БД по URL: {db_url.split('@')[0]}@***")
    try:
        await Tortoise.init(
            db_url=db_url,
            modules={'models': ['Database.Models']}
        )
        await Tortoise.generate_schemas()
    except Exception as e:
        logger.error(f"Ошибка инициализации базы данных: {e}")
        raise


class Database:
    """
    Класс для работы с базой данных пользователей.
    Использует Tortoise ORM для асинхронного взаимодействия.
    """

    async def add_user(self, user_id: int, user_name: str) -> None:
        """
        Добавляет нового пользователя в базу данных, если его ещё нет.
        
        Args:
            user_id: ID пользователя (обычно из Telegram)
            user_name: Имя пользователя
        """
        user = await User.get_or_none(id=user_id)
        if user is None:
            await User.create(id=user_id, name=user_name)

    async def get_name(self, user_id: int) -> str | None:
        """
        Получает имя пользователя по его ID.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Имя пользователя или None, если пользователь не найден
        """
        user = await User.get_or_none(id=user_id)
        return user.name if user else None

    async def subscribe(self, user_id: int) -> None:
        """
        Увеличивает счётчик подписчиков пользователя на 1.
        
        Args:
            user_id: ID пользователя
        """
        user = await User.get_or_none(id=user_id)
        if user:
            user.subscribers += 1
            await user.save()

    async def get_subscribe(self, user_id: int) -> int:
        """
        Получает количество подписчиков пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Количество подписчиков (0, если пользователь не найден)
        """
        user = await User.get_or_none(id=user_id)
        return user.subscribers if user else 0

    async def set_token(self, user_id: int, token: str) -> None:
        """
        Устанавливает или обновляет токен пользователя.
        
        Args:
            user_id: ID пользователя
            token: Новый токен
        """
        user = await User.get_or_none(id=user_id)
        if user:
            user.token = token
            await user.save()

    async def get_token(self, user_id: int) -> str | None:
        """
        Получает токен пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Токен пользователя или None
        """
        user = await User.get_or_none(id=user_id)
        return user.token if user else None

    async def main_sub(self) -> int:
        """
        Получает общее количество пользователей в системе.
        
        Returns:
            Количество всех пользователей
        """
        return await User.all().count()

    async def increment_message_count(self, owner_id: int) -> None:
        """
        Увеличивает счётчик сообщений пользователя на 1.
        
        Args:
            owner_id: ID владельца бота (пользователя)
        """
        user = await User.get_or_none(id=owner_id)
        if user:
            user.total_messages = (user.total_messages or 0) + 1
            await user.save()

    async def register_bot_user(self, owner_id: int, bot_user_id: int) -> None:
        """
        Регистрирует нового пользователя для бота владельца.
        Увеличивает счётчик уникальных пользователей для владельца.
        
        Args:
            owner_id: ID владельца бота
            bot_user_id: ID пользователя, который написал боту
        """
        # Проверяем, есть ли уже такая запись
        existing = await BotUser.get_or_none(owner_id=owner_id, user_id=bot_user_id)
        
        if existing is None:
            # Создаём новую запись о пользователе
            await BotUser.create(owner_id=owner_id, user_id=bot_user_id)
            
            # Увеличиваем счётчик уникальных пользователей
            owner = await User.get_or_none(id=owner_id)
            if owner:
                owner.total_users = (owner.total_users or 0) + 1
                await owner.save()

    async def get_stats(self, user_id: int) -> tuple[int, int]:
        """
        Получает статистику пользователя (сообщения и пользователи).
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Кортеж (total_messages, total_users) или (0, 0) если пользователь не найден
        """
        user = await User.get_or_none(id=user_id)
        if user:
            return (user.total_messages or 0, user.total_users or 0)
        return (0, 0)
