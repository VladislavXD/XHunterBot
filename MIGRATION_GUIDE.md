# 📋 Руководство по миграции БД

## ✅ Что было сделано

Логика базы данных перенесена из `app/Database.py` в `app/Database/` папку с использованием **Tortoise ORM** вместо **aiosqlite**.

### Структура нового кода:

```
app/Database/
├── __init__.py          # Экспорт Database и init
├── DB.py               # Класс Database с методами
└── Models.py           # Модели User и BotUser
```

---

## 🔄 Основные изменения

### 1. **Асинхронность**
- ✅ Весь код использует `async/await` через Tortoise ORM
- ✅ Поддержка PostgreSQL и SQLite
- ✅ Автоматическое создание таблиц через `generate_schemas()`

### 2. **Новые модели**

#### User (существующая, расширенная)
```python
class User(Model):
    id = fields.BigIntField(pk=True)
    name = fields.TextField(null=True)
    token = fields.TextField(null=True)
    subscribers = fields.IntField(default=0)
    total_messages = fields.IntField(default=0)
    total_users = fields.IntField(default=0)
    # ... другие поля
```

#### BotUser (новая для отслеживания пользователей ботов)
```python
class BotUser(Model):
    owner_id = fields.BigIntField()
    user_id = fields.BigIntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        unique_together = (("owner_id", "user_id"),)
```

---

## 🚀 Как использовать

### 1. Инициализация БД в main.py:

```python
import asyncio
from Database import Database, init as init_db

async def main():
    # Инициализируем БД при запуске
    await init_db()
    
    # Затем можно использовать Database
    db = Database()
    await db.add_user(user_id=123, user_name="John")
    
    # ... остальной код

if __name__ == '__main__':
    asyncio.run(main())
```

### 2. Использование методов Database:

```python
db = Database()

# Добавить пользователя
await db.add_user(user_id=123, user_name="Alice")

# Получить имя
name = await db.get_name(123)

# Получить статистику
messages, users = await db.get_stats(123)

# Увеличить счётчики
await db.subscribe(123)
await db.increment_message_count(123)

# Регистрация пользователя бота
await db.register_bot_user(owner_id=123, bot_user_id=456)
```

---

## 📝 Переменные окружения

### Для PostgreSQL (рекомендуется):

```bash
DATABASE_URL=postgres://user:password@localhost:5432/xhunter_db

# Или отдельные переменные:
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=xhunter_db
```

### Для SQLite (по умолчанию):

```bash
# Используется db.sqlite3 в корне проекта
# Переменные окружения не требуются
```

---

## 🔧 Миграция существующих данных

Если у вас есть старая БД в SQLite, нужна миграция:

```python
# 1. Экспортируем из старой БД
import aiosqlite

async def migrate_data():
    # Читаем из старой БД
    async with aiosqlite.connect('./database.db') as old_db:
        cursor = await old_db.execute("SELECT id, name, token, subscribers FROM users")
        users = await cursor.fetchall()
    
    # Записываем в новую БД (Tortoise)
    from Database.Models import User
    for user_id, name, token, subscribers in users:
        await User.create(
            id=user_id,
            name=name,
            token=token,
            subscribers=subscribers
        )
```

---

## ✨ Преимущества нового подхода

| Характеристика | Старое (aiosqlite) | Новое (Tortoise) |
|---|---|---|
| **ORM** | ❌ Нет, SQL запросы | ✅ Да, моделированные объекты |
| **Безопасность** | ⚠️ SQL Injection возможен | ✅ Параметризованные запросы |
| **Валидация** | ❌ Нет | ✅ Встроенная валидация полей |
| **Миграции** | ❌ Ручные | ✅ Автоматические `generate_schemas()` |
| **Поддержка БД** | SQLite только | ✅ PostgreSQL, MySQL, SQLite и др. |
| **Удобство** | Объекты БД | ✅ Работа с моделями как объектами |

---

## ⚠️ Важно

1. **Удалите старый файл** `app/Database.py` - больше не используется
2. **Убедитесь**, что все импорты обновлены на `from Database import ...`
3. **Инициализируйте БД** в точке входа через `await init_db()`
4. **Используйте переменные окружения** для конфигурации

---

## 🐛 Возможные проблемы

### Ошибка: "Не удается разрешить импорт Database"

**Решение:** Убедитесь, что в папке `Database/` есть файл `__init__.py`

### Ошибка: "No module named 'tortoise'"

**Решение:** Установите зависимость:
```bash
pip install tortoise-orm aiosqlite asyncpg  # asyncpg для PostgreSQL
```

### БД не инициализируется

**Решение:** Вызовите `await init_db()` в асинхронной функции при запуске:
```python
async def main():
    await init_db()  # Это необходимо!
    # ... остальной код
```

---

## 📚 Дополнительные ресурсы

- [Tortoise ORM Documentation](https://tortoise-orm.readthedocs.io/)
- [Модели в Tortoise](https://tortoise-orm.readthedocs.io/en/latest/fields.html)
- [Асинхронные операции](https://tortoise-orm.readthedocs.io/en/latest/query.html)
