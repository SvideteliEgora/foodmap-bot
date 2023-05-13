from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from loader import dp, bot
from states.main_states import MainStatesGroup
from aiogram.dispatcher import FSMContext
from murkups.main_murkups import ikb_main


@dp.callback_query_handler(Text(startswith='main_next_'), state=MainStatesGroup.main)
async def cb_next(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['current_page'] = int(callback.data[10:])

        feeding_products = data.get('feeding_products')
        current_page = data.get('current_page')
        products_on_page = data.get('products_on_page')
        user_weight = data.get('user_weight')
        date = data.get('date')
        count_proteins = data.get('count_proteins')
        daily_proteins = data.get('daily_proteins')
        count_fats = data.get('count_fats')
        daily_fats = data.get('daily_fats')
        count_carbohydrates = data.get('count_carbohydrates')
        daily_carbohydrates = data.get('daily_carbohydrates')
        count_calories = data.get('count_calories')
        daily_calories = data.get('daily_calories')

    product_text = "\n\n".join(feeding_products[(current_page - 1) * products_on_page:current_page * products_on_page])

    await callback.message.edit_text(text=f'Ваш текущий вес: {user_weight} кг\n\n'
                                          f'Дата: {date.today()}\n\n'
                                          f'{product_text}\n\n'
                                          f'ИТОГО:        Б/Ж/У - {count_proteins}/{daily_proteins} {count_fats}/{daily_fats} {count_carbohydrates}/{daily_carbohydrates}\n'
                                          f'                      Ккал - {count_calories}/{daily_calories}\n'
                                          f'                      Вода - 2150 мл',
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=ikb_main(feeding_products, current_page))


@dp.callback_query_handler(Text(startswith='main_back_'), state=MainStatesGroup.main)
async def cb_back(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['current_page'] = int(callback.data[10:])

        feeding_products = data.get('feeding_products')
        current_page = data.get('current_page')
        products_on_page = data.get('products_on_page')
        user_weight = data.get('user_weight')
        date = data.get('date')
        count_proteins = data.get('count_proteins')
        daily_proteins = data.get('daily_proteins')
        count_fats = data.get('count_fats')
        daily_fats = data.get('daily_fats')
        count_carbohydrates = data.get('count_carbohydrates')
        daily_carbohydrates = data.get('daily_carbohydrates')
        count_calories = data.get('count_calories')
        daily_calories = data.get('daily_calories')

    product_text = "\n\n".join(feeding_products[(current_page - 1) * products_on_page:current_page * products_on_page])

    await callback.message.edit_text(text=f'Ваш текущий вес: {user_weight} кг\n\n'
                                          f'Дата: {date.today()}\n\n'
                                          f'{product_text}\n\n'
                                          f'ИТОГО:        Б/Ж/У - {count_proteins}/{daily_proteins} {count_fats}/{daily_fats} {count_carbohydrates}/{daily_carbohydrates}\n'
                                          f'                      Ккал - {count_calories}/{daily_calories}\n'
                                          f'                      Вода - 2150 мл',
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=ikb_main(feeding_products, current_page))