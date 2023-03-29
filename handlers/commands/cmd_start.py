from aiogram.dispatcher.filters import CommandStart
from loader import dp, bot, UsersDB
from aiogram import types
from aiogram.types import ReplyKeyboardRemove


@dp.message_handler(CommandStart())
async def cmd_start(message: types.Message) -> None:
    if(not UsersDB.user_exists(user_id=message.from_user.id)):
        await bot.send_message(chat_id=message.from_user.id,
                               text='Привет добро пожаловать в фуд бот!')

    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Привет! Рад снова тебя видеть!')