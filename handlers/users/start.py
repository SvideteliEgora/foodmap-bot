from aiogram.dispatcher.filters import CommandStart
from loader import dp, bot, UsersDB
from aiogram import types
from murkups.profile_markups import create_profile_kb
from murkups.menu_markups import menu_kb


@dp.message_handler(CommandStart())
async def cmd_start(message: types.Message) -> None:
    if(not UsersDB.user_exists(user_id=message.from_user.id)):
        await bot.send_message(chat_id=message.from_user.id,
                               text='Привет добро пожаловать в фуд бот!\n'
                                    'Для начала, вам необходимо создать профиль.\n'
                                    'Чтобы создать профиль - введите /create и заполните анкету.',
                               reply_markup=create_profile_kb)

    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Привет! Рад снова тебя видеть!',
                               reply_markup=menu_kb)