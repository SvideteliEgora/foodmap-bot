from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ADD_OR_DELETE_PRODUCT_IKB = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Добавить продукт', callback_data='main_product_add'),
     InlineKeyboardButton('Удалить продукт', callback_data='main_product_delete')],
])