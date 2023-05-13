from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


IKB_ADD_USER_PRODUCTS = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Добавить продукт', callback_data='main_product_add')],
])


def ikb_get_user_products(products: dict, current_page=1) -> InlineKeyboardMarkup:

    # Создаем клавиатуру
    ikb = InlineKeyboardMarkup()


    # Определяем количество кнопок на странице
    buttons_on_page = 10
    pages_count = (len(products) - 1) // buttons_on_page + 1

    # Заполняем первую страницу кнопок
    for product in products[:buttons_on_page]:
        ikb.add(InlineKeyboardButton(product.get("title"), callback_data=product.get("id")))

    # Если кнопок больше, чем на одной странице, добавляем кнопки "Далее" и "Счетчик страниц"
    if len(products) > buttons_on_page:
        ikb.add(InlineKeyboardButton(f"{current_page} / {pages_count}", callback_data='pages_count'))
        ikb.insert(InlineKeyboardButton(f">>", callback_data=f"user_products_next_{current_page + 1}"))

    if current_page > 1:
        ikb.inline_keyboard = []
        for product in products[(current_page - 1) * buttons_on_page:current_page * buttons_on_page]:
            ikb.add(InlineKeyboardButton(product.get("title"), callback_data=product.get("id")))

        # Добавляем кнопки "<<", "счетчик страниц", ">>"
        ikb.add(InlineKeyboardButton("<<", callback_data=f"user_products_back_{current_page - 1}"))
        ikb.insert(InlineKeyboardButton(f"{current_page} / {pages_count}", callback_data='pages_count'))

        if current_page < pages_count:
            ikb.insert(InlineKeyboardButton(f">>", callback_data=f"user_products_next_{current_page + 1}"))

    return ikb
