from loader import dp
from aiogram import types
from loader import UserFeedingDB, ProductsDB
from aiogram.dispatcher.filters import Text
from states.main_states import MainStatesGroup
from aiogram.dispatcher import FSMContext
from murkups.main_murkups import ikb_delete_product_from_main
from functions.get_total_calories import total_product_value
from loader import UserFeedingDB


@dp.callback_query_handler(Text(equals='main_product_delete'), state=MainStatesGroup.main)
async def cb_delete_product_from_main(callback: types.CallbackQuery, state: FSMContext):

    # Продукты добавленные пользователем, как съеденные сегодня
    # user_feeding_today = UserFeedingDB.get_feeding_today(callback.from_user.id)
    #
    # products = []
    #
    # for product in user_feeding_today:
    #     product_id = product.get('product_id')
    #     product_weight = product.get('product_weight')
    #     feeding_time = product.get('feeding_time')
    #
    #     # Находим название продукта по product_id
    #     product_info = ProductsDB.get_product(product_id)
    #     product_title = product_info.get('title')
    #
    #     products.append({
    #         product_id: f"{feeding_time}, {product_title}, {product_weight}г"
    #     })
    async with state.proxy() as data:
        feeding_products_data = data.get('feeding_products_data')

    await callback.message.edit_text(text='Выберете продукт, который вы хотите удалить из сегодняшнего дня:',
                                     reply_markup=ikb_delete_product_from_main(feeding_products_data))


@dp.callback_query_handler(Text(startswith='next_del_'), state=MainStatesGroup.main)
async def cb_next_page_del(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['current_page'] += 1
        feeding_products_data = data.get('feeding_products_data')

    await callback.message.edit_reply_markup(reply_markup=ikb_delete_product_from_main(feeding_products_data,
                                                                                       data.get('current_page')))


@dp.callback_query_handler(Text(startswith='back_del_'), state=MainStatesGroup.main)
async def cb_back_page_del(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['current_page'] -= 1
        feeding_products_data = data.get('feeding_products_data')

    await callback.message.edit_reply_markup(reply_markup=ikb_delete_product_from_main(feeding_products_data,
                                                                                       data.get('current_page')))


@dp.callback_query_handler(Text(startswith='feeding_id_'), state=MainStatesGroup.main)
async def cb_product_selection_and_del(callback: types.CallbackQuery, state: FSMContext):
    feeding_id = callback.data[11:]
    UserFeedingDB.del_eaten_product(feeding_id)

    await callback.answer(text='⏳⏳⏳')
    await state.finish()
    await callback.message.edit_text(text='Продукт успешно удален!')
