from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from functions.profile_functions import calculate_daily_calories, verify_number, calculate_daily_pfc, calculate_daily_water_allowance
from loader import bot, dp, UserProfilesDB
from murkups.profile_markups import target_ikb, active_ikb, gender_ikb
from states import CreateProfileStatesGroup


@dp.callback_query_handler(Text(equals='create_profile'))
async def started_create_profile(callback: types.Message) -> None:
    await CreateProfileStatesGroup.name.set()
    await callback.bot.send_message(chat_id=callback.from_user.id,
                                    text='Твое имя:')


# check name
@dp.message_handler(lambda message: not (message.text.isalpha() or len(message.text) >= 15),
                    state=CreateProfileStatesGroup.name)
async def check_name(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='<em>Некоректные данные</em>\n'
                                'Имя может содержать только букенные символы, в колличестве не больше 15.')
    await message.delete()


# load name, next age
@dp.message_handler(state=CreateProfileStatesGroup.name)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text.title()

    await CreateProfileStatesGroup.next()
    await bot.send_message(chat_id=message.from_user.id,
                           text="Сколько вам лет?\n\n",
                           parse_mode='HTML')
    await message.delete()


# check age
@dp.message_handler(lambda message: not message.text.isdigit(), state=CreateProfileStatesGroup.age)
async def check_age(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='<em>Некоректные данные.</em>\n\n'
                                'Вам нужно указать свой возраст (лет).\n'
                                'Это должно быть <b>целое число</b>, не меньше 8',
                           parse_mode='HTML')
    await message.delete()


# load age, next weight
@dp.message_handler(state=CreateProfileStatesGroup.age)
async def load_age(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['age'] = int(message.text)

    await CreateProfileStatesGroup.next()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Введите ваш вес <em>(кг)</em>:',
                           parse_mode='HTML')
    await message.delete()


# check weight
@dp.message_handler(lambda message: not verify_number(message.text), state=CreateProfileStatesGroup.weight)
async def check_weight(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='<em>Некоректные данные</em>\n\n'
                                'Вам нужно указать свой вес <em>(кг)</em>.'
                                'Это должно быть <b>целое (75)</b> или <b>дробное число (75.5)</b>',
                           parse_mode='HTML')
    await message.delete()


# load weight, next height
@dp.message_handler(state=CreateProfileStatesGroup.weight)
async def load_weight(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if message.text.isdigit():
            data['weight'] = int(message.text)
        else:
            data['weight'] = round(float(message.text))

    await CreateProfileStatesGroup.next()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Введите ваш рост <em>(см)</em>:',
                           parse_mode='HTML')
    await message.delete()


# check height
@dp.message_handler(lambda message: not verify_number(message.text), state=CreateProfileStatesGroup.height)
async def check_height(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='<em>Некоректные данные</em>\n\n'
                                'Введите ваш рост. Это должно быть <b>целое (75)</b> или <b>дробное число (75.5)</b>',
                           parse_mode='HTML')
    await message.delete()


# load height, next gender
@dp.message_handler(state=CreateProfileStatesGroup.height)
async def load_height(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if message.text.isdigit():
            data['height'] = int(message.text)
        else:
            data['height'] = round(float(message.text))

    await CreateProfileStatesGroup.next()
    await bot.send_message(chat_id=message.from_user.id,
                           text="Укажите ваш пол:",
                           reply_markup=gender_ikb)
    await message.delete()


# check gender
@dp.message_handler(state=CreateProfileStatesGroup.gender)
async def check_gender(message: types.Message) -> None:
    await message.delete()


# load gender
@dp.callback_query_handler(state=CreateProfileStatesGroup.gender)
async def load_gender(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['gender'] = callback.data

    await CreateProfileStatesGroup.next()
    await callback.message.edit_text(text="Какая у вас цель?\n\n"
                                          "выберете ответ:",
                                     reply_markup=target_ikb)


# check target
@dp.message_handler(state=CreateProfileStatesGroup.target)
async def check_target(message: types.Message) -> None:
    await message.delete()


# load target, next active
@dp.callback_query_handler(state=CreateProfileStatesGroup.target)
async def load_target(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['target'] = callback.data
    await CreateProfileStatesGroup.next()
    await callback.message.edit_text(text="Укажите вашу активность:",
                                     reply_markup=active_ikb)


# check active
@dp.message_handler(state=CreateProfileStatesGroup.active)
async def check_target(message: types.Message) -> None:
    await message.delete()


#load active
@dp.callback_query_handler(state=CreateProfileStatesGroup.active)
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

        daily_calories = calculate_daily_calories(weight=data['weight'], height=data['height'],
                                                  age=data['age'], active=data['active'],
                                                  gender=data['gender'], target=data['target'])

        daily_water_allowance = calculate_daily_water_allowance(weight=data['weight'])
        daily_pfc = calculate_daily_pfc(daily_calories, {'proteins': 30, 'fats': 30, 'carbohydrates': 40})

        data['daily_pfc'] = daily_pfc['daily_pfc_string']
        data['daily_calories'] = daily_calories
        data['daily_water_allowance'] = daily_water_allowance

    UserProfilesDB.add_user(user_id=callback.from_user.id, data=data)
    await state.finish()
    await callback.message.edit_text(text='Данные профиля сохранены!\n\n'
                                          'Теперь вы можете добавлять продукты и следить за своим питанием!\n'
                                          'Для этого воспользуйтесь командами в меню.')
