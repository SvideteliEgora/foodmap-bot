from loader import dp, UserFeedingDB
from aiogram import types
from aiogram.dispatcher.filters import Text
from states.product_states import ProductsStatesGroup
from aiogram.dispatcher import FSMContext
from functions.get_total_calories import total_product_value
from aiogram.types import ParseMode, ReplyKeyboardRemove


@dp.callback_query_handler(Text(equals='add_product'), state=ProductsStatesGroup.choose_product)
async def add_product(callback: types.CallbackQuery, state: FSMContext):
    await ProductsStatesGroup.add_product_weight.set()
    await callback.message.answer(text='Укажите вес продукта:')


@dp.message_handler(state=ProductsStatesGroup.add_product_weight)
async def add_product_weight(message: types.Message, state: FSMContext):
    product_weight = message.text
    async with state.proxy() as data:

        product = total_product_value(product_id=data['select_product']['id'],
                                      product_title=data['select_product']['title'],
                                      protein=data['select_product']['proteins'],
                                      fats=data['select_product']['fats'],
                                      carbohydrates=data['select_product']['carbohydrates'],
                                      calories=data['select_product']['calories'],
                                      total_weight=product_weight)
        await state.finish()

        # Добавляем продукт в БД (user_feeding)
        UserFeedingDB.add_eaten_product(product_id=product.get('id'), user_id=message.from_user.id,
                                        product_weight=product_weight)
        await message.answer(text=f'<b>{product.get("title")}, {product.get("weight")} g</b> - добавлено!\n',
                             parse_mode=ParseMode.HTML,
                             reply_markup=ReplyKeyboardRemove())
