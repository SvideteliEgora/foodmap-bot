from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


# def get_products_kb(data: dict) -> ReplyKeyboardMarkup:
#     kb = ReplyKeyboardMarkup(resize_keyboard=True)
#     count = 0
#     for item in data:
#         kb.add(KeyboardButton(item['title']))
#         count += 1
#     return kb


def search_products_kb(products: dict, current_page=1) -> ReplyKeyboardMarkup:

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
        for product in products[(current_page - 1) * buttons_on_page:current_page * buttons_on_page]:
            keyboard.add(KeyboardButton(product["title"]))

        # Добавляем кнопки "Назад" и "Далее"
        if current_page > 1:
            keyboard.add(KeyboardButton(f"{current_page - 1} <-- Назад"))
        if current_page < pages_count:
            keyboard.add(KeyboardButton(f"Далее --> {current_page + 1}"))

    return keyboard




        # # Обновляем сообщение с клавиатурой
        # await bot.edit_message_reply_markup(chat_id=message.chat.id,
        #                                     message_id=message.message_id,
        #                                     reply_markup=keyboard)

#         # Если выбран продукт, отправляем информацию о нем
#     elif search_choice.result in [product["title"] for product in products]:
#         product = BotProductsDB.get_product(message.text)
#         await message.answer(f"Название: {product['title']}\n"
#                              f"Цена: {product['сalories']}\n"
#                              f"Описание: {product['proteins']}")
#
#     return keyboard
#
#
# def

    #
    # # # Ждем ответа от пользователя
    # # async with dp.message_handler(Text()) as search_choice:
    #     # Если выбрана кнопка "Далее", переходим на следующую страницу
    #     while search_choice.result == "Далее" and current_page < pages_count:
    #         current_page += 1
    #
    #         # Очищаем клавиатуру и заполняем ее кнопками предыдущей страницы
    #
    #
