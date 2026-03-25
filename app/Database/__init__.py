"""
Модуль Database для работы с Tortoise ORM.
Содержит инициализацию БД и класс Database с методами.
"""

from .DB import Database, init

__all__ = ['Database', 'init']
