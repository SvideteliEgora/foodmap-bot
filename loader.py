from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
import asyncio

from db import UsersDB, FeedingDB, ProductsDB



loop = asyncio.get_event_loop()
bot = Bot(token=config.TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, loop, storage)
UsersDB = UsersDB('foodmap.db')
FeedingDB = FeedingDB('foodmap.db')
ProductsDB = ProductsDB('foodmap.db')

