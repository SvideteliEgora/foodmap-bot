from loader import dp, bot, UserProfilesDB
from aiogram import types


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    if(not UserProfilesDB.user_exists(user_id=message.from_user.id)):
        await bot.send_message(chat_id=message.from_user.id,
                               text='Привет добро пожаловать в фуд бот!')

    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Привет! Рад снова тебя видеть!')
