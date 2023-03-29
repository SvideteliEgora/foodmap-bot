from aiogram.dispatcher.filters import Command
from loader import dp, bot, UsersDB
from aiogram import types
from states.profile_states import CreateProfileStatesGroup
from murkups.profile_markups import edit_profile_ikb


@dp.message_handler(Command('profile'))
async def cmd_profile(message: types.Message) -> None:
    if(not UsersDB.user_exists(user_id=message.from_user.id)):
        await bot.send_message(chat_id=message.from_user.id,
                               text='У тебя пока нет прфиля. Давай создадим его.\n'
                                    'Напиши, как тебя зовут: (например: Вадим)')
        await CreateProfileStatesGroup.name.set()
    else:
        user_profile = UsersDB.get_user_profile(message.from_user.id)

        await bot.send_message(chat_id=message.from_user.id,
                               text=f"<em>Имя</em>: <b>{user_profile['name']}</b>\n"
                                    f"<em>Пол</em>: <b>{user_profile['gender']}</b>\n"
                                    f"<em>Возраст</em>: <b>{user_profile['age']} лет</b>\n"
                                    f"<em>Вес</em>: <b>{user_profile['weight']} кг</b>\n"
                                    f"<em>Рост</em>: <b>{user_profile['height']} см</b>\n"
                                    f"<em>Уровень активности</em>: <b>{user_profile['active']}</b>\n"
                                    f"<em>Цель</em>: <b>{user_profile['target']}</b>\n\n"
                                    f"<em>Ежедневная норма </em>: <b>{user_profile['daily_calories']} ккал</b>\n"
                                    f"<em>Ежедневный объем воды</em>: <b>{user_profile['daily_water_allowance']} мл</b>\n"
                                    f"<em>Соотношение БЖУ</em>: <b>{user_profile['daily_bzhu']}</b>",
                               parse_mode='HTML',
                               reply_markup=edit_profile_ikb)
    await message.delete()