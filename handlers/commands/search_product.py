from loader import bot, dp
from aiogram import types
from loader import UserProfilesDB
from murkups.profile_markups import CREATE_PROFILE
from states.product_states import ProductsStatesGroup


@dp.message_handler(commands=['searchproduct'])
async def search_products(message: types.Message) -> None:
    if not UserProfilesDB.user_exists(user_id=message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text='Для использования всех возможностей бота, в том числе поиска продуктов, '
                                    'тебе необходимо создать профиль.',
                               reply_markup=CREATE_PROFILE)
    else:
        await ProductsStatesGroup.search_product.set()
        await bot.send_message(chat_id=message.from_user.id,
                               text='введи продукт:')
    await message.delete()