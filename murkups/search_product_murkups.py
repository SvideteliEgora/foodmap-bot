from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def add_product_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('+', callback_data='add_product')]
    ])

    return ikb


def get_results_search_products_kb(products: dict, current_page=1) -> ReplyKeyboardMarkup:

    # Создаем клавиатуру
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)


    # Определяем количество кнопок на странице
    buttons_on_page = 50
    pages_count = (len(products) - 1) // buttons_on_page + 1

    # Заполняем первую страницу кнопок
    for product in products[:buttons_on_page]:
        keyboard.add(KeyboardButton(product["title"]))

    # Если кнопок больше, чем на одной странице, добавляем кнопку "Далее"
    if len(products) > buttons_on_page:
        keyboard.add(KeyboardButton(f"Далее --> {current_page + 1}"))

    if current_page > 1:
        keyboard.keyboard = []
        keyboard.add(KeyboardButton(f"{current_page - 1} <-- Назад"))
        for product in products[(current_page - 1) * buttons_on_page:current_page * buttons_on_page]:
            keyboard.add(KeyboardButton(product["title"]))

        # Добавляем кнопки "Назад" и "Далее"
        if current_page < pages_count:
            keyboard.add(KeyboardButton(f"Далее --> {current_page + 1}"))

    return keyboard


