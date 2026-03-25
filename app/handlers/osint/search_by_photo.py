from telebot import types
from create_bot import bot
from handlers.state import UserState
from handlers.setLanguage import get_text
from handlers.buttons import back

import os
import tempfile
import shutil
import asyncio
from pathlib import Path
from utils.reverse_search import search_saucenao


@bot.callback_query_handler(func=lambda call: call.data == 'search_photo')
async def open_search_photo_page(call: types.CallbackQuery):
	"""Open the Search Photo page and set user state to accept photo input."""
	chat_id = call.message.chat.id
	language = UserState.get_language(chat_id)
	img = open('./img/main.jpeg', 'rb')
	media = types.InputMediaPhoto(media=img, caption=get_text('search_photo_page', language))
	try:
		await bot.edit_message_media(chat_id=chat_id, message_id=call.message.message_id, media=media, reply_markup=back(chat_id))
	finally:
		img.close()

	# set waiting state — user should send a photo or a link
	UserState.search_photo[chat_id] = {'search_photo': True, 'page_message_id': call.message.message_id}
	await bot.answer_callback_query(call.id, 'OK')


@bot.message_handler(func=lambda message: UserState.search_photo.get(message.chat.id, {}).get('search_photo', False), content_types=['photo', 'document', 'text'])
async def process_search_photo(message: types.Message):
	"""Process an incoming photo or image URL and run reverse image search (SauceNAO).

	Requirements:
	  - set environment variable SAUCENAO_API_KEY with your SauceNAO API key.
	"""
	print(f"DEBUG: process_search_photo called for chat {message.chat.id}")  # debug
	chat_id = message.chat.id

	# reset waiting flag immediately
	UserState.search_photo.get(chat_id, {})['search_photo'] = False

	language = UserState.get_language(chat_id)

	tmpdir = tempfile.mkdtemp(prefix='revimg_')
	try:
		img_path = None

		# 1) If user sent a photo via Telegram
		if getattr(message, 'photo', None):
			# get biggest photo
			file_id = message.photo[-1].file_id
			try:
				file_info = await bot.get_file(file_id)
				file_bytes = await bot.download_file(file_info.file_path)
			except Exception as e:
				await bot.send_message(chat_id, f"❌ Failed to download photo from Telegram: {e}", reply_markup=back(chat_id))
				return

			img_path = os.path.join(tmpdir, 'photo.jpg')
			with open(img_path, 'wb') as fh:
				fh.write(file_bytes)

		# 2) If user sent a document (image file)
		elif getattr(message, 'document', None) and message.document.mime_type.startswith('image'):
			file_id = message.document.file_id
			try:
				file_info = await bot.get_file(file_id)
				file_bytes = await bot.download_file(file_info.file_path)
			except Exception as e:
				await bot.send_message(chat_id, f"❌ Failed to download document: {e}", reply_markup=back(chat_id))
				return
			ext = Path(message.document.file_name).suffix or '.jpg'
			img_path = os.path.join(tmpdir, f'photo{ext}')
			with open(img_path, 'wb') as fh:
				fh.write(file_bytes)

		# 3) If user sent a URL as text — try to download
		elif message.text and message.text.startswith(('http://', 'https://')):
			url = message.text.strip()
			await bot.send_message(chat_id, get_text('searching', language).format(username='image'), reply_markup=back(chat_id))
			try:
				import aiohttp
				async with aiohttp.ClientSession() as session:
					async with session.get(url, timeout=30) as resp:
						if resp.status != 200:
							await bot.send_message(chat_id, f'❌ Failed to download image: HTTP {resp.status}', reply_markup=back(chat_id))
							return
						content = await resp.read()
						# try to infer extension
						ct = resp.headers.get('Content-Type', '')
						ext = '.jpg'
						if 'png' in ct:
							ext = '.png'
						elif 'gif' in ct:
							ext = '.gif'
						img_path = os.path.join(tmpdir, f'photo{ext}')
						with open(img_path, 'wb') as fh:
							fh.write(content)
			except Exception as e:
				await bot.send_message(chat_id, f"❌ Error downloading URL: {e}", reply_markup=back(chat_id))
				return

		else:
			await bot.send_message(chat_id, get_text('no_results', language), reply_markup=back(chat_id))
			return

		# Ensure we have an image file
		if not img_path or not os.path.exists(img_path):
			await bot.send_message(chat_id, '❌ Image not found after download.', reply_markup=back(chat_id))
			return

		# Check for SauceNAO API key
		import os as _os
		api_key = _os.getenv('SAUCENAO_API_KEY', '').strip()
		if not api_key:
			await bot.send_message(chat_id, (
				'� Для поиска по изображению требуется API-ключ SauceNAO.\n'
				'Пожалуйста, установите SAUCENAO_API_KEY в окружении сервера.'
			), reply_markup=back(chat_id))
			return

		await bot.send_message(chat_id, '⏳ Выполняю обратный поиск по изображению...', reply_markup=back(chat_id))

		try:
			results = await search_saucenao(img_path, api_key, numres=8)
		except Exception as e:
			await bot.send_message(chat_id, f'❌ Ошибка поиска: {e}', reply_markup=back(chat_id))
			return

		if not results:
			await bot.send_message(chat_id, get_text('no_results', language), reply_markup=back(chat_id))
			return

		# Build inline keyboard with top results (use first ext_url if available)
		markup = types.InlineKeyboardMarkup(row_width=1)
		for r in results:
			title = r.get('title') or r.get('index_name') or 'Result'
			sim = r.get('similarity') or ''
			urls = r.get('ext_urls') or []
			target = urls[0] if urls else r.get('thumbnail')
			if not target:
				continue
			text = f"{sim}% {title}" if sim else title
			try:
				btn = types.InlineKeyboardButton(text=text[:60], url=target)
				markup.add(btn)
			except Exception:
				# skip malformed url
				continue

		caption = f"🔎 Найдено результатов: {len(markup.keyboard)}"
		await bot.send_message(chat_id, caption, reply_markup=markup)

	finally:
		shutil.rmtree(tmpdir, ignore_errors=True)
