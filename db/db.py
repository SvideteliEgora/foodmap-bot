import sqlite3
from aiogram.utils.exceptions import ChatNotFound
from aiogram import Dispatcher


class DB:

    def __init__(self, db_file):
        """Инициализация соединения с БД"""
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def get_all_data(self, table_name) -> list:
        """Получение всех данных из таблицы"""
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    @staticmethod
    def is_user_valid(self, user_id) -> bool:
        try:
            int(user_id)
            return True
        except ValueError:
            return False

    @staticmethod
    async def is_chat_valid(chat_id, dp: Dispatcher) -> bool:
        try:
            await dp.bot.get_chat(int(chat_id))
        except ChatNotFound:
            return False
        return True








