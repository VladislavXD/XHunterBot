from tortoise import fields
from tortoise import Model



class User(Model):
	id = fields.BigIntField(pk=True)
	name = fields.TextField(null=True)
	token = fields.TextField(null=True)
	subscribers = fields.IntField(default=0)
	total_messages = fields.IntField(default=0)
	total_users = fields.IntField(default=0)
	premium = fields.BooleanField(default=False)
	username = fields.CharField(max_length=32, null=True)
	chat_id = fields.BigIntField(unique=True, null=True)
	created_at = fields.DatetimeField(auto_now_add=True)
	updated_at = fields.DatetimeField(auto_now=True)
	last_active = fields.DatetimeField(null=True)
	is_banned = fields.BooleanField(default=False)
	language = fields.CharField(max_length=10, null=True)
	referral_code = fields.CharField(max_length=64, null=True)
	referred_by = fields.CharField(max_length=64, null=True)
	notes = fields.TextField(null=True)


class BotUser(Model):
	"""
	Модель для отслеживания уникальных пользователей каждого бота.
	
	Структура:
	- owner_id: ID владельца бота (из таблицы User)
	- user_id: ID пользователя, взаимодействующего с ботом
	- Первичный ключ: (owner_id, user_id) - гарантирует уникальность
	"""
	owner_id = fields.BigIntField()
	user_id = fields.BigIntField()
	created_at = fields.DatetimeField(auto_now_add=True)

	class Meta:
		# Составной первичный ключ
		unique_together = (("owner_id", "user_id"),)
