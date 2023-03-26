from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
menu_kb.add(KeyboardButton('Профиль 👤'), KeyboardButton('Главная 🟢')).add\
          (KeyboardButton('Итоги'), KeyboardButton('Мои продукты')).add\
          (KeyboardButton('О Боте 🤖'))


back_to_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
back_to_menu_kb.add(KeyboardButton('Меню 🔙'))


