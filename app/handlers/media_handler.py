import os
import tempfile
import shutil
import asyncio
from create_bot import bot
from telebot import types
from .state import UserState
from utils.media_utils import download_with_yt_dlp, download_instagram_post


# Расширяемая карта провайдеров: ключ -> функция загрузки (sync)
# Добавить новый провайдер: импортируйте функцию в media_utils и добавьте сюда соответствие
PROVIDERS = {
    'instagram': download_instagram_post,
    'default': download_with_yt_dlp,
}


def detect_provider(url: str) -> str:
    """Возвращает ключ провайдера по URL.

    При добавлении нового провайдера можно расширить логику определения.
    """
    if 'instagram.com' in url:
        return 'instagram'
    # можно добавить 'youtube.com', 'tiktok.com' и т.д.
    return 'default'


# NOTE: The /download command handler was intentionally removed.
# The bot should accept download URLs as plain text while the user
# is on the "download" page. The active message handler below
# (listening based on UserState.waiting_for_download_url) performs
# the actual processing.


async def process_download(chat_id: int, url: str):
    """Универсальная функция для скачивания и отправки медиа по URL."""
    tmpdir = tempfile.mkdtemp(prefix="media_")
    try:
        provider_key = detect_provider(url)
        downloader = PROVIDERS.get(provider_key, PROVIDERS['default'])

        # Для Instagram сначала пробуем yt_dlp (быстрее и чаще работает),
        # затем — instaloader как запасной вариант. Для остальных провайдеров
        # используем назначенный загрузчик.
        filepath = None
        last_exc = None
        if provider_key == 'instagram':
            downloaders = [PROVIDERS['default'], PROVIDERS['instagram']]
        else:
            downloaders = [downloader]

        for dl in downloaders:
            try:
                filepath = await asyncio.to_thread(dl, url, tmpdir)
                break
            except Exception as e:
                last_exc = e
                # пробуем следующий загрузчик
                continue

        if not filepath:
            msg = str(last_exc) if last_exc else 'Unknown error'
            # даём пользователю полезную подсказку только если оба метода не сработали
            if 'Fetching Post metadata failed' in msg or 'Instaloader failed' in msg or '401' in msg or '403' in msg:
                await bot.send_message(chat_id, "❌ Не удалось получить данные поста Instagram. Попробуйте задать INSTALOADER_USER и INSTALOADER_PASS в окружении (если это приватный пост) или повторите попытку позже.")
            else:
                await bot.send_message(chat_id, f"❌ Ошибка при загрузке: {msg}")
            return

        # Отправляем файл
        if not os.path.exists(filepath):
            await bot.send_message(chat_id, "❌ Файл не найден после загрузки.")
            return
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        caption = os.path.basename(filepath)
        await bot.send_message(chat_id, f"✅ Загружено: {caption} ({size_mb:.1f} MB). Отправляю в чат...")

        # Всегда отправляем как документ для надежности
        with open(filepath, 'rb') as fh:
            await bot.send_document(chat_id, fh, caption=caption)

        
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


@bot.message_handler(func=lambda message: UserState.waiting_for_download_url.get(message.chat.id, False))
async def handle_download_message(message: types.Message):
    url = message.text.strip()
    chat_id = message.chat.id
    # снимаем состояние
    UserState.waiting_for_download_url.pop(chat_id, None)

    await bot.send_message(chat_id, f"⏳ Обрабатываю: {url}")
    try:
        await process_download(chat_id, url)
    except Exception as e:
        await bot.send_message(chat_id, f"❌ Ошибка при обработке URL: {e}")
