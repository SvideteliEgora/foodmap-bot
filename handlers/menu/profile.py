from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from functions.profile_functions import get_calculate_bzhu, verify_number
from loader import bot, dp, UsersDB
from murkups.profile_markups import create_profile_kb, cancel_create_profile_kb, target_ikb, active_ikb, gender_ikb
from states import ProfileStatesGroup
from murkups.menu_markups import menu_kb


@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext) -> None:
    if state is None:
        return

    await state.finish()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Вы прервали саздание профиля.',
                           reply_markup=create_profile_kb)


@dp.message_handler(commands=['create'])
async def cmd_create(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='Ваше имя:',
                           reply_markup=cancel_create_profile_kb)
    await ProfileStatesGroup.name.set()
    await message.delete()


# check name
@dp.message_handler(lambda message: not (message.text.isalpha() or len(message.text) >= 15), state=ProfileStatesGroup.name)
async def check_name(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='<em>Некоректные данные</em>\n'
                                'Имя может содержать только букенные символы, в колличестве не больше 15.')
    await message.delete()


# load name, next age
@dp.message_handler(state=ProfileStatesGroup.name)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text.title()

    await ProfileStatesGroup.next()
    await bot.send_message(chat_id=message.from_user.id,
                           text="Сколько вам лет?\n\n",
                           parse_mode='HTML')
    await message.delete()


# check age
@dp.message_handler(lambda message: not message.text.isdigit(), state=ProfileStatesGroup.age)
async def check_age(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='<em>Некоректные данные.</em>\n\n'
                                'Вам нужно указать свой возраст (лет).\n'
                                'Это должно быть <b>целое число</b>, не меньше 8',
                           parse_mode='HTML')
    await message.delete()


# load age, next weight
@dp.message_handler(state=ProfileStatesGroup.age)
async def load_age(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['age'] = int(message.text)

    await ProfileStatesGroup.next()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Введите ваш вес <em>(кг)</em>:',
                           parse_mode='HTML')
    await message.delete()


# check weight
@dp.message_handler(lambda message: not verify_number(message.text), state=ProfileStatesGroup.weight)
async def check_weight(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='<em>Некоректные данные</em>\n\n'
                                'Вам нужно указать свой вес <em>(кг)</em>.'
                                'Это должно быть <b>целое (75)</b> или <b>дробное число (75.5)</b>',
                           parse_mode='HTML')
    await message.delete()


# load weight, next height
@dp.message_handler(state=ProfileStatesGroup.weight)
async def load_weight(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if message.text.isdigit():
            data['weight'] = int(message.text)
        else:
            data['weight'] = round(float(message.text))

    await ProfileStatesGroup.next()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Введите ваш рост <em>(см)</em>:',
                           parse_mode='HTML')
    await message.delete()


# check height
@dp.message_handler(lambda message: not verify_number(message.text), state=ProfileStatesGroup.height)
async def check_height(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='<em>Некоректные данные</em>\n\n'
                                'Введите ваш рост. Это должно быть <b>целое (75)</b> или <b>дробное число (75.5)</b>',
                           parse_mode='HTML')
    await message.delete()


# load height, next gender
@dp.message_handler(state=ProfileStatesGroup.height)
async def load_height(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if message.text.isdigit():
            data['height'] = int(message.text)
        else:
            data['height'] = round(float(message.text))

    await ProfileStatesGroup.next()
    await bot.send_message(chat_id=message.from_user.id,
                           text="Укажите ваш пол:",
                           reply_markup=gender_ikb)
    await message.delete()


# check gender
@dp.message_handler(state=ProfileStatesGroup.gender)
async def check_gender(message: types.Message) -> None:
    await message.delete()


# load gender
@dp.callback_query_handler(state=ProfileStatesGroup.gender)
async def load_gender(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['gender'] = callback.data

    await ProfileStatesGroup.next()
    await callback.message.edit_text(text="Какая у вас цель?\n\n"
                                          "выберете ответ:",
                                     reply_markup=target_ikb)


# check target
@dp.message_handler(state=ProfileStatesGroup.target)
async def check_target(message: types.Message) -> None:
    await message.delete()


# load target, next active
@dp.callback_query_handler(state=ProfileStatesGroup.target)
async def load_target(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['target'] = callback.data
    await ProfileStatesGroup.next()
    await callback.message.edit_text(text="Укажите вашу активность:\n\n"
                                          "1. Никаких физических нагрузок\n"
                                          "2. Физические нагрузки 1-3 раза в неделю\n"
                                          "3. Физические нагрузки 3-5 раз в неделю\n"
                                          "4. Физические нагрузки 6-7 раз в неделю\n"
                                          "5. Тренировки чаще, чем раз в день\n",
                                     parse_mode='HTML',
                                     reply_markup=active_ikb)


# check active
@dp.message_handler(state=ProfileStatesGroup.active)
async def check_target(message: types.Message) -> None:
    await message.delete()


#load active
@dp.callback_query_handler(state=ProfileStatesGroup.active)
async def load_active(callback: types.CallbackQuery, state: FSMContext) -> None:
    activity_levels = {
        "no_activity": "Никаких физических нагрузок",
        "light_activity": "Физические нагрузки 1-3 раза в неделю",
        "moderate_activity": "Физические нагрузки 3-5 раз в неделю",
        "heavy_activity": "Физические нагрузки 6-7 раз в неделю",
        "very_heavy_activity": "Тренировки чаще, чем раз в день",
    }
    async with state.proxy() as data:
        data['active'] = activity_levels[callback.data]
    calories, pfc = get_calculate_bzhu(weight=data['weight'], height=data['height'], age=data['age'],
                                       active=data['active'], gender=data['gender'], target=data['target'])
    UsersDB.add_user(user_id=callback.from_user.id, data=data)
    await state.finish()
    await callback.message.edit_text(text='Ваш профиль успешно создан!')
    await callback.message.answer(text=f"Ваш профиль:\n\n"
                                f"<em>Имя</em>: <b>{data['name']}</b>\n"
                                f"<em>Пол</em>: <b>{data['gender']}</b>\n"
                                f"<em>Возраст</em>: <b>{data['age']} лет</b>\n"
                                f"<em>Вес</em>: <b>{data['weight']} кг</b>\n"
                                f"<em>Рост</em>: <b>{data['height']} см</b>\n"
                                f"<em>Уровень активности</em>: <b>{data['active']}</b>\n"
                                f"<em>Цель</em>: <b>{data['target']}</b>\n\n"
                                f"<em>Ежедневная норма </em>: <b>{calories} ккал</b>\n"
                                f"<em>Ежедневный объем воды</em>: <b>... мл</b>\n"
                                f"<em>Соотношение БЖУ</em>: <b>30/30/40</b>",
                           parse_mode='HTML',
                           reply_markup=menu_kb)


@dp.message_handler(Text(equals="Профиль 👤"))
async def profile(message: types.Message):
    user_profile = UsersDB.get_user_profile(message.from_user.id)

    data = {
        'name': user_profile[1],
        'gender': user_profile[2],
        'age': user_profile[3],
        'weight': user_profile[4],
        'height': user_profile[5],
        'active': user_profile[6],
        'target': user_profile[7]
    }

    await message.answer(text=f"Ваш профиль:\n\n"
                                f"<em>Имя</em>: <b>{data['name']}</b>\n"
                                f"<em>Пол</em>: <b>{data['gender']}</b>\n"
                                f"<em>Возраст</em>: <b>{data['age']} лет</b>\n"
                                f"<em>Вес</em>: <b>{data['weight']} кг</b>\n"
                                f"<em>Рост</em>: <b>{data['height']} см</b>\n"
                                f"<em>Уровень активности</em>: <b>{data['active']}</b>\n"
                                f"<em>Цель</em>: <b>{data['target']}</b>\n\n"
                                f"<em>Ежедневная норма </em>: <b>/// ккал</b>\n"
                                f"<em>Ежедневный объем воды</em>: <b>... мл</b>\n"
                                f"<em>Соотношение БЖУ</em>: <b>30/30/40</b>",
                           parse_mode='HTML',
                           reply_markup=menu_kb)

    await message.delete()