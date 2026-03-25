from middleware.middleware import check_subscription_decorator
from telebot import types
from create_bot import bot
from handlers.state import UserState
from handlers.setLanguage import get_text
from handlers.buttons import back
from utils.search_by_name import search_wmn
import asyncio


PER_PAGE = 20


def _build_results_markup(results, chat_id, page=0):
	markup = types.InlineKeyboardMarkup(row_width=1)
	start = page * PER_PAGE
	slice_ = results[start:start + PER_PAGE]
	for name, url in slice_:
		try:
			markup.add(types.InlineKeyboardButton(name, url=url))
		except Exception:
			continue

	# navigation
	nav = []
	total_pages = (len(results) + PER_PAGE - 1) // PER_PAGE
	language = UserState.get_language(chat_id)
	prev_label = get_text('pagination_prev', language)
	next_label = get_text('pagination_next', language)
	if page > 0:
		nav.append(types.InlineKeyboardButton(prev_label, callback_data=f'search_user_page:{page-1}'))
	if page < total_pages - 1:
		nav.append(types.InlineKeyboardButton(next_label, callback_data=f'search_user_page:{page+1}'))

	if nav:
		markup.row(*nav)

	# back button
	markup.add(types.InlineKeyboardButton(get_text('back_btn', UserState.get_language(chat_id)), callback_data='back'))
	return markup


@bot.message_handler(func=lambda message: UserState.search_user.get(message.chat.id, {}).get('search_user', False))
async def process_search_user(message: types.Message):
	"""Handle username search input, call utils.search_by_name.search_wmn and show results on the same page.

	Results are shown as URL buttons with pagination; the original page message is edited to keep UI consistent.
	"""
	chat_id = message.chat.id
	username = message.text.strip()

	# Сбрасываем ожидание ввода
	UserState.search_user[chat_id]['search_user'] = False

	language = UserState.get_language(chat_id)
	await bot.send_message(chat_id, get_text('searching', language).format(username=username))

	try:
		results = await search_wmn(username)
	except Exception as e:
		await bot.send_message(chat_id, f"❌ Ошибка при поиске: {e}")
		return

	if not results:
		await bot.send_message(chat_id, get_text('no_results', UserState.get_language(chat_id)), reply_markup=back(chat_id))
		return

	# Сохраняем результаты в состоянии пользователя для пагинации
	UserState.search_user[chat_id].update({'results': results, 'username': username, 'page': 0})

	# Построим markup для первой страницы и отредактируем страницу
	markup = _build_results_markup(results, chat_id, page=0)
	page_id = UserState.search_user.get(chat_id, {}).get('page_message_id')
	img = open('./img/main.jpeg', 'rb')
	caption = get_text('search_results', language).format(username=username, count=len(results))
	media = types.InputMediaPhoto(media=img, caption=caption)

	try:
		if page_id:
			await bot.edit_message_media(chat_id=chat_id, message_id=page_id, media=media, reply_markup=markup)
		else:
			await bot.send_photo(chat_id, img, caption=caption, reply_markup=markup)
	finally:
		img.close()


@bot.callback_query_handler(func=lambda call: call.data and call.data.startswith('search_user_page:'))
async def _handle_search_user_page(call: types.CallbackQuery):
	"""Pagination handler for search results pages."""
	try:
		page = int(call.data.split(':', 1)[1])
	except Exception:
		await bot.answer_callback_query(call.id, 'Invalid page')
		return

	chat_id = call.message.chat.id
	state = UserState.search_user.get(chat_id)
	if not state or 'results' not in state:
		await bot.answer_callback_query(call.id, 'Нет данных для пагинации')
		return

	results = state['results']
	total_pages = (len(results) + PER_PAGE - 1) // PER_PAGE
	if page < 0 or page >= total_pages:
		await bot.answer_callback_query(call.id, 'Страница вне диапазона')
		return

	state['page'] = page
	markup = _build_results_markup(results, chat_id, page=page)
	username = state.get('username', '')
	language = UserState.get_language(chat_id)

	img = open('./img/main.jpeg', 'rb')
	caption = get_text('search_results', language).format(username=username, count=len(results)) + f" (страница {page+1}/{total_pages})"
	media = types.InputMediaPhoto(media=img, caption=caption)
	try:
		await bot.edit_message_media(chat_id=chat_id, message_id=call.message.message_id, media=media, reply_markup=markup)
		await bot.answer_callback_query(call.id)
	finally:
		img.close()
