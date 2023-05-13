from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


IKB_ADD_PRODUCT = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Добавить продукт', callback_data='main_product_add')],
])


def ikb_main(products: list, current_page=1) -> InlineKeyboardMarkup:

    # Создаем клавиатуру
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Добавить продукт', callback_data='main_product_add'),
         InlineKeyboardButton('Удалить продукт', callback_data='main_product_delete')],
    ])


    # Определяем количество записей о съеденных продуктах на странице
    products_on_page = 5
    pages_count = (len(products) - 1) // products_on_page + 1

    # Если записей больше, чем на одной странице, добавляем кнопки "Cчетчик страниц" и ">>"
    if len(products) > products_on_page:
        ikb.add(InlineKeyboardButton(f"{current_page} / {pages_count}", callback_data='pages_count'))
        ikb.insert(InlineKeyboardButton(f">>", callback_data=f"main_next_{current_page + 1}"))

    if current_page > 1:
        ikb.inline_keyboard = []
        ikb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton('Добавить продукт', callback_data='main_product_add'),
             InlineKeyboardButton('Удалить продукт', callback_data='main_product_delete')],
        ])
        ikb.add(InlineKeyboardButton(f"<<", callback_data=f"main_back_{current_page - 1}"))
        ikb.insert(InlineKeyboardButton(f"{current_page} / {pages_count}", callback_data='pages_count'))
        if current_page < pages_count:
            ikb.insert(InlineKeyboardButton(f">>", callback_data=f'main_next_{current_page + 1}'))

    return ikb


def ikb_delete_product_from_main(products: list, current_page=1) -> InlineKeyboardMarkup:

    # Создаем клавиатуру
    ikb = InlineKeyboardMarkup()


    # Определяем количество кнопок на странице
    buttons_on_page = 5
    pages_count = (len(products) - 1) // buttons_on_page + 1

    # Заполняем первую страницу кнопок
    for product in products[:buttons_on_page]:
        product_title = product.get('product_title')
        feeding_id = product.get('feeding_id')
        product_weight = product.get('product_weight')
        feeding_time = product.get('feeding_time')

        ikb.add(InlineKeyboardButton(f"{feeding_time}, {product_title}, {product_weight}г",
                                     callback_data=f"feeding_id_{feeding_id}"))

    # Если кнопок больше, чем на одной странице, добавляем кнопки "Далее" и "Счетчик страниц"
    if len(products) > buttons_on_page:
        ikb.add(InlineKeyboardButton(f"{current_page} / {pages_count}", callback_data='pages_count'))
        ikb.insert(InlineKeyboardButton(f">>", callback_data=f"next_del_{current_page + 1}"))

    if current_page > 1:
        ikb.inline_keyboard = []
        for product in products[(current_page - 1) * buttons_on_page:current_page * buttons_on_page]:
            product_title = product.get('product_title')
            feeding_id = product.get('feeding_id')
            product_weight = product.get('product_weight')
            feeding_time = product.get('feeding_time')

            ikb.add(InlineKeyboardButton(f"{feeding_time}, {product_title}, {product_weight}г",
                                         callback_data=f"feeding_id_{feeding_id}"))

        # Добавляем кнопки "<<", "счетчик страниц", ">>"
        ikb.add(InlineKeyboardButton("<<", callback_data=f"back_del_{current_page - 1}"))
        ikb.insert(InlineKeyboardButton(f"{current_page} / {pages_count}", callback_data='pages_count_del'))

        if current_page < pages_count:
            ikb.insert(InlineKeyboardButton(f">>", callback_data=f"next_del_{current_page + 1}"))

    return ikb