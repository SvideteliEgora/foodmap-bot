from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loader import bot, dp, ProductsDB
from aiogram import types
from loader import UserProfilesDB
from murkups.search_product_murkups import get_results_search_products_kb, add_product_ikb
from murkups.profile_markups import CREATE_PROFILE
from functions.get_total_calories import total_product_value
from states.product_states import ProductsStatesGroup


@dp.message_handler(state=ProductsStatesGroup.search_product)
async def search_products(message: types.Message, state: FSMContext):
    if not UserProfilesDB.user_exists(user_id=message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text='Для использования всех возможностей бота, в том числе поиска продуктов, '
                                    'тебе необходимо создать профиль.',
                               reply_markup=CREATE_PROFILE)
        return

    # Находим все продукты, которые содержат искомую строку
    products = ProductsDB.find_products(message.text)

    # Если список продуктов пуст, отправляем сообщение, что ничего не найдено
    if not products:
        await message.answer("Ничего не найдено")
        return

    await ProductsStatesGroup.choose_product.set()
    async with state.proxy() as data:
        data['current_page'] = 1
        data['pages_count'] = (len(products) - 1) // 10 + 1
        data['search_products'] = products

    # Отправляем сообщение с клавиатурой
    await message.answer("Выбери подходящий вариант:", reply_markup=get_results_search_products_kb(products))


@dp.callback_query_handler(Text(startswith='next_'), state=ProductsStatesGroup.choose_product)
async def next_page(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['current_page'] += 1
    await callback.message.edit_text(text="Выбери подходящий вариант:",
                                     reply_markup=get_results_search_products_kb(data['search_products'], data['current_page']))


@dp.callback_query_handler(Text(endswith='_back'), state=ProductsStatesGroup.choose_product)
async def back_page(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['current_page'] -= 1
    await callback.message.edit_text(text="Выберете подходящий вариант:",
                                     reply_markup=get_results_search_products_kb(data['search_products'], data['current_page']))


@dp.callback_query_handler(state=ProductsStatesGroup.choose_product)
async def choose_product(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        for item in data['search_products']:
            if item.get('id') == int(callback.data):
                data['select_product'] = item
                await callback.message.answer(text=f"{item['title']}\n"
                                          f"На 100 грамм:\n"
                                          f"Калорийность - {item['calories']}\n"
                                          f"Белки - {item['proteins']}\n"
                                          f"Жиры - {item['fats']}\n"
                                          f"Углеводы - {item['carbohydrates']}\n",
                                     reply_markup=add_product_ikb())
                return
        else:
            # Находим все продукты, которые содержат искомую строку
            products = ProductsDB.find_products(callback.message.text)

            # Если список продуктов пуст, отправляем сообщение, что ничего не найдено
            if not products:
                await callback.message.answer("Ничего не найдено")
                return

            await ProductsStatesGroup.choose_product.set()
            async with state.proxy() as data:
                data['current_page'] = 1
                data['pages_count'] = (len(products) - 1) // 50 + 1
                data['search_products'] = products

            # Отправляем сообщение с клавиатурой
            await callback.message.answer("Выбери подходящий вариант:", reply_markup=get_results_search_products_kb(products))