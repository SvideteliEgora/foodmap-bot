from loader import dp
from aiogram.dispatcher.filters import Text
from aiogram import types
from states.product_state import ProductsStatesGroup


@dp.callback_query_handler(Text(equals='main_product_add'))
async def add_product(callback: types.CallbackQuery):
    await ProductsStatesGroup.search_product.set()
    await callback.message.answer(text='Введите название продукта:')