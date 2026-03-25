import os
import glob
import yt_dlp
import instaloader
import shutil
from typing import Optional


def download_with_yt_dlp(url: str, tmpdir: str) -> str:
    """Скачивает видео через yt_dlp в tmpdir и возвращает путь к файлу."""
    opts = {
        'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',  # Гибкий формат с ограничением качества
        'noplaylist': True,
        'quiet': True,
        'geo_bypass': True,  # Обход гео-ограничений
        'extractor_args': {'youtube': {'player_skip': ['js']}},
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])

    files = glob.glob(os.path.join(tmpdir, '**', '*.*'), recursive=True)
    if not files:
        raise RuntimeError("Файл не найден после загрузки yt_dlp")
    return max(files, key=os.path.getsize)


def download_instagram_post(url: str, tmpdir: str, username: Optional[str] = None, password: Optional[str] = None) -> str:
    """Скачивает пост Instagram через instaloader в tmpdir и возвращает путь к файлу."""
    L = instaloader.Instaloader(download_videos=True, save_metadata=False, dirname_pattern=tmpdir)

    username = username or os.getenv("INSTALOADER_USER")
    password = password or os.getenv("INSTALOADER_PASS")
    if username and password:
        L.login(username, password)
		
		
    shortcode = url.rstrip('/').split('/')[-1]
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    L.download_post(post, target=tmpdir)

    files = glob.glob(os.path.join(tmpdir, '**', '*.*'), recursive=True)
    media = next((f for f in files if f.lower().endswith(('.mp4', '.mov', '.webm'))), None)
    if not media and files:
        media = files[0]
    if not media:
        raise RuntimeError("Медиа не найдено после скачивания Instagram поста")
    return media
