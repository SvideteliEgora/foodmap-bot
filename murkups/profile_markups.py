from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


create_profile_kb = ReplyKeyboardMarkup(resize_keyboard=True)
create_profile_kb.add(KeyboardButton('/create'))


cancel_create_profile_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_create_profile_kb.add(KeyboardButton('/cancel'))


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
    [InlineKeyboardButton("1", callback_data="no_activity"), InlineKeyboardButton("2", callback_data="light_activity")],
    [InlineKeyboardButton("3", callback_data="moderate_activity"), InlineKeyboardButton("4", callback_data="heavy_activity")],
    [InlineKeyboardButton("5", callback_data="very_heavy_activity")]
])
