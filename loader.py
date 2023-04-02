from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
import asyncio

from db import UserProfilesDB, UserFeedingDB, UserProductsDB, ProductsDB



loop = asyncio.get_event_loop()
bot = Bot(token=config.TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, loop, storage)
UserProfilesDB = UserProfilesDB('foodmap.db')
UserFeedingDB = UserFeedingDB('foodmap.db')
UserProductsDB = UserProductsDB('foodmap.db')
ProductsDB = ProductsDB('foodmap.db')

