from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


CREATE_PROFILE = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Создать', callback_data="create_profile")]
])


target_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("Cнизить вес", callback_data="Снизить вес")],
    [InlineKeyboardButton("Набрать вес", callback_data="Набрать вес")],
    [InlineKeyboardButton("Поддерживать вес", callback_data="Поддерживать вес")]
])


gender_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("Мужской", callback_data="Мужской")],
    [InlineKeyboardButton("Женский", callback_data="Женский")]
])


active_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("1. Никаких физических нагрузок", callback_data="no_activity"),
     InlineKeyboardButton("2. Физические нагрузки 1-3 раза в неделю", callback_data="light_activity")],
    [InlineKeyboardButton("3. Физические нагрузки 3-5 раз в неделю", callback_data="moderate_activity"),
     InlineKeyboardButton("4. Физические нагрузки 6-7 раз в неделю", callback_data="heavy_activity")],
    [InlineKeyboardButton("5. Тренировки чаще, чем раз в день", callback_data="very_heavy_activity")]
])


edit_profile_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Изменить данные профиля', callback_data="edit_profile_data")]
])


params_edit_profile_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Имя', callback_data='up_name'), InlineKeyboardButton('Пол', callback_data='up_gender'),
     InlineKeyboardButton('Возраст', callback_data='up_age'), InlineKeyboardButton('Вес', callback_data='up_weight')],
    [InlineKeyboardButton('Рост', callback_data='up_height'), InlineKeyboardButton('Активность', callback_data='up_active'),
     InlineKeyboardButton('Цель', callback_data='up_target')],
    [InlineKeyboardButton('Норма калорий', callback_data='up_daily_calories'),
     InlineKeyboardButton('Объем воды', callback_data='up_daily_water_allowance'), InlineKeyboardButton('БЖУ', callback_data='up_bzhu')]
])

