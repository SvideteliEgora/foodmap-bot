from loader import dp, UserProductsDB
from aiogram import types
from murkups.user_products_murkups import IKB_ADD_USER_PRODUCTS, ikb_get_user_products


@dp.message_handler(commands=['myproducts'], state='*')
async def cmd_add_product(message: types.Message):
    if not(UserProductsDB.user_products_exists(message.from_user.id)):
        await message.answer(text='Вы не добавили ни одного продукта.',
                             reply_markup=IKB_ADD_USER_PRODUCTS)
    else:
        all_user_products = UserProductsDB.get_all_products(message.from_user.id)
        await message.answer(text='Список ваших продуктов:',
                             reply_markup=ikb_get_user_products(all_user_products))