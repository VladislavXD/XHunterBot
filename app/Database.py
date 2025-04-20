import sqlite3
import threading
import aiosqlite

class Database:
    def __init__(self, db_file):
        self.db_file = db_file

    async def add_user(self, user_id, user_name):
        async with aiosqlite.connect(self.db_file) as db:
            cursor = await db.execute("SELECT 1 FROM users WHERE id = ?", (user_id,))
            result = await cursor.fetchone()
            
            if result is None:
                await db.execute("INSERT INTO users (id, name) VALUES (?, ?)", (user_id, user_name))
                await db.commit()

    async def get_name(self, user_id):
        async with aiosqlite.connect(self.db_file) as db:
            cursor = await db.execute("SELECT name FROM users WHERE id = ?", (user_id,))
            result = await cursor.fetchone()
            return result[0] if result else None

    async def subscribe(self, user_id):
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute("UPDATE users SET subscribers = subscribers + 1 WHERE id = ?", (user_id,))
            await db.commit()

    async def get_subscribe(self, user_id):
        async with aiosqlite.connect(self.db_file) as db:
            cursor = await db.execute("SELECT subscribers FROM users WHERE id = ?", (user_id,))
            result = await cursor.fetchone()
            return result[0] if result else 0

    async def set_token(self, user_id, token):
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute("UPDATE users SET token = ? WHERE id = ?", (token, user_id))
            await db.commit()

    async def get_token(self, user_id):
        async with aiosqlite.connect(self.db_file) as db:
            cursor = await db.execute("SELECT token FROM users WHERE id = ?", (user_id,))
            result = await cursor.fetchone()
            return result[0] if result else None

    async def main_sub(self):
        async with aiosqlite.connect(self.db_file) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM users")
            result = await cursor.fetchone()
            return result[0] if result else 0


    
    
    
    async def increment_message_count(self, owner_id: int):
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute("""
                UPDATE users
                SET total_messages = COALESCE(total_messages, 0) + 1
                WHERE id = ?
            """, (owner_id,))
            await db.commit()

    async def register_bot_user(self, owner_id: int, bot_user_id: int):
        async with aiosqlite.connect(self.db_file) as db:
            # Таблица bot_users для отслеживания уникальных пользователей каждого бота
            await db.execute('''
                CREATE TABLE IF NOT EXISTS bot_users (
                    owner_id INTEGER,
                    user_id INTEGER,
                    PRIMARY KEY (owner_id, user_id)
                )
            ''')
            # Проверка: был ли уже этот пользователь
            cursor = await db.execute("""
                SELECT 1 FROM bot_users WHERE owner_id = ? AND user_id = ?
            """, (owner_id, bot_user_id))
            result = await cursor.fetchone()

            if result is None:
                await db.execute("INSERT INTO bot_users (owner_id, user_id) VALUES (?, ?)", (owner_id, bot_user_id))
                await db.execute("""
                    UPDATE users
                    SET total_users = COALESCE(total_users, 0) + 1
                    WHERE id = ?
                """, (owner_id,))
                await db.commit()

    async def get_stats(self, user_id):
        async with aiosqlite.connect(self.db_file) as db:
            cursor = await db.execute("""
                SELECT total_messages, total_users FROM users WHERE id = ?
            """, (user_id,))
            result = await cursor.fetchone()
            return result if result else (0, 0)
