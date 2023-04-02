from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from functions.profile_functions import calculate_daily_calories, verify_number
from loader import bot, dp, UserProfilesDB
from murkups.profile_markups import target_ikb, active_ikb, gender_ikb, params_edit_profile_ikb, edit_profile_ikb
from states import EditProfileStatesGroup


@dp.callback_query_handler(Text(equals='edit_profile_data'))
async def edit_profile_cb(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=params_edit_profile_ikb)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('up_'))
async def edit_one_param_profile_cb(callback: types.CallbackQuery):
    if callback.data == 'up_name':
        await EditProfileStatesGroup.name.set()
        await callback.message.answer(text='Введите новое имя:')
    elif callback.data == 'up_gender':
        await EditProfileStatesGroup.gender.set()
        await callback.message.answer(text='Укажите ваш пол:',
                                      reply_markup=gender_ikb)
    elif callback.data == 'up_age':
        await EditProfileStatesGroup.age.set()
        await callback.message.answer(text='Введите ваш возраст:')

    elif callback.data == 'up_weight':
        await EditProfileStatesGroup.weight.set()
        await callback.message.answer(text='Введите новый вес:')

    elif callback.data == 'up_height':
        await EditProfileStatesGroup.height.set()
        await callback.message.answer(text='Введите новый рост:')

    elif callback.data == 'up_active':
        await EditProfileStatesGroup.active.set()
        await callback.message.answer(text="Укажите вашу активность:",
                                      reply_markup=active_ikb)

    elif callback.data == 'up_target':
        await EditProfileStatesGroup.target.set()
        await callback.message.answer(text='Укажите новую цель:',
                                      reply_markup=target_ikb)

    elif callback.data == 'up_daily_calories':
        await EditProfileStatesGroup.daily_calories.set()
        await callback.message.answer(text='Введите вашу суточную норму калорий:')

    elif callback.data == 'up_daily_water_allowance':
        await EditProfileStatesGroup.daily_water_allowance.set()
        await callback.message.answer(text='Введите вашу суточную норму воды:')

    elif callback.data == 'up_bzhu':
        await EditProfileStatesGroup.bzhu.set()
        await callback.message.answer(text='Введите значение для БЖУ через пробел. (например: 30 30 40)')


# check new name
@dp.message_handler(lambda message: not (message.text.isalpha() or len(message.text) >= 15),
                    state=EditProfileStatesGroup.name)
async def check_new_name(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='Имя может содержать только букенные символы, в колличестве не больше 15.'
                           )
    await message.delete()


# update name
@dp.message_handler(state=EditProfileStatesGroup.name)
async def update_name(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    UserProfilesDB.update_one_user_param(user_id=message.from_user.id, column='name', value=message.text.title())
    await bot.send_message(chat_id=message.from_user.id,
                           text="Имя успешно изменено!")
    await message.delete()


# check new age
@dp.message_handler(lambda message: not message.text.isdigit(), state=EditProfileStatesGroup.age)
async def check_new_age(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='<em>Некоректные данные.</em>\n\n'
                                'Вам нужно указать свой возраст (лет).\n'
                                'Это должно быть <b>целое число</b>, не меньше 8',
                           parse_mode='HTML')
    await message.delete()


# update age
@dp.message_handler(state=EditProfileStatesGroup.age)
async def update_age(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    UserProfilesDB.update_one_user_param(user_id=message.from_user.id, column='age', value=message.text.title())
    await bot.send_message(chat_id=message.from_user.id,
                           text='Возраст успешно изменен!')
    await message.delete()


# check new weight
@dp.message_handler(lambda message: not verify_number(message.text), state=EditProfileStatesGroup.weight)
async def check_weight(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='<em>Некоректные данные</em>\n\n'
                                'Вам нужно указать свой вес <em>(кг)</em>.'
                                'Это должно быть <b>целое (75)</b> или <b>дробное число (75.5)</b>',
                           parse_mode='HTML')
    await message.delete()


# update weight
@dp.message_handler(state=EditProfileStatesGroup.weight)
async def update_weight(message: types.Message, state: FSMContext) -> None:
    if message.text.isdigit():
        value = int(message.text)
    else:
        value = round(float(message.text))

    await state.finish()
    UserProfilesDB.update_one_user_param(user_id=message.from_user.id, column='weight', value=value)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Вес успешно изменен!')
    await message.delete()


# check new height
@dp.message_handler(lambda message: not verify_number(message.text), state=EditProfileStatesGroup.height)
async def check_new_height(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='<em>Некоректные данные</em>\n\n'
                                'Введите ваш рост. Это должно быть <b>целое (75)</b> или <b>дробное число (75.5)</b>',
                           parse_mode='HTML')
    await message.delete()


# update height
@dp.message_handler(state=EditProfileStatesGroup.height)
async def update_height(message: types.Message, state: FSMContext) -> None:
    if message.text.isdigit():
        value = int(message.text)
    else:
        value = round(float(message.text))

    await state.finish()
    UserProfilesDB.update_one_user_param(user_id=message.from_user.id, column='height', value=value)
    await bot.send_message(chat_id=message.from_user.id,
                           text="Рост успешно изменен")
    await message.delete()


# check new gender
@dp.message_handler(state=EditProfileStatesGroup.gender)
async def check_new_gender(message: types.Message) -> None:
    await message.delete()


# update gender
@dp.callback_query_handler(state=EditProfileStatesGroup.gender)
async def update_gender(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.finish()
    UserProfilesDB.update_one_user_param(user_id=callback.from_user.id, column='gender', value=callback.data)
    await callback.message.edit_text(text="Пол успешно изменен!")


# check new target
@dp.message_handler(state=EditProfileStatesGroup.target)
async def check_new_target(message: types.Message) -> None:
    await message.delete()


# update target
@dp.callback_query_handler(state=EditProfileStatesGroup.target)
async def update_target(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.finish()
    UserProfilesDB.update_one_user_param(user_id=callback.from_user.id, column='target', value=callback.data)
    await callback.message.edit_text(text="Цель успешно изменена!")


# check new active
@dp.message_handler(state=EditProfileStatesGroup.active)
async def check_new_target(message: types.Message) -> None:
    await message.delete()


#update active
@dp.callback_query_handler(state=EditProfileStatesGroup.active)
async def update_active(callback: types.CallbackQuery, state: FSMContext) -> None:
    activity_levels = {
        "no_activity": "Никаких физических нагрузок",
        "light_activity": "Физические нагрузки 1-3 раза в неделю",
        "moderate_activity": "Физические нагрузки 3-5 раз в неделю",
        "heavy_activity": "Физические нагрузки 6-7 раз в неделю",
        "very_heavy_activity": "Тренировки чаще, чем раз в день",
    }

    await state.finish()
    UserProfilesDB.update_one_user_param(user_id=callback.from_user.id, column='active', value=activity_levels[callback.data])
    await callback.message.edit_text(text='Ваша активность успешно изменена!')


