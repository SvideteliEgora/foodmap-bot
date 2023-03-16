from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,InlineKeyboardButton, InlineKeyboardMarkup


# menu
def get_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Профиль 👤'), KeyboardButton('Главная 🟢')).add\
          (KeyboardButton('Тренировка 🏋️'), KeyboardButton('О Боте 🤖'))

    return kb


# back to menu
def get_back_to_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Меню 🔙'))

    return kb


# create profile
def get_create_profile_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/create'))

    return kb


# cancel create profile
def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/cancel'))

    return kb

# Инлайн клавиатуры
# gender_cb = CallbackData('gender_ikb', 'action')
# ikb_gender = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton('Мужской', callback_data='Мужской')],
#         [InlineKeyboardButton('Женский', callback_data='Женский')]
# ])


ikb_target = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Снизить вес', callback_data='Снизить вес')],
    [InlineKeyboardButton('Набрать вес', callback_data='Набрать вес')],
    [InlineKeyboardButton('Поддерживать вес', callback_data='Поддерживать вес')]
])


ikb_workout = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Минимальный уровень (никаких физических нагрузок)', callback_data='Минимальный уровень (никаких физических нагрузок)')],
    [InlineKeyboardButton('Низкий (физические нагрузки 1-3 раза в неделю)', callback_data='Низкий (физические нагрузки 1-3 раза в неделю)')],
    [InlineKeyboardButton('Средний (физические нагрузки 3-5 раз в неделю)', callback_data='Средний (физические нагрузки 3-5 раз в неделю)')],
    [InlineKeyboardButton('Высокий (физические нагрузки 6-7 раз в неделю)', callback_data='Высокий (физические нагрузки 6-7 раз в неделю)')],
    [InlineKeyboardButton('Очень высокий (тренировки чаще, чем раз в день)', callback_data='Очень высокий (тренировки чаще, чем раз в день)')],

])