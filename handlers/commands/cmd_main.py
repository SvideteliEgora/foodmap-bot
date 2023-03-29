from aiogram.dispatcher.filters import Command, Text, state
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from loader import dp, bot, UsersDB, BotProductsDB
from aiogram import types
from states.profile_states import CreateProfileStatesGroup
from states.main_state import MainStatesGroup
from aiogram.dispatcher import FSMContext
from murkups.main_markups import search_products_kb


@dp.message_handler(Command('main'))
async def cmd_profile(message: types.Message) -> None:
    if not UsersDB.user_exists(user_id=message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text='У тебя пока нет прфиля. Давай создадим его.\n'
                                    'Напиши, как тебя зовут: (например: Вадим)')
        await CreateProfileStatesGroup.name.set()
    else:
        await MainStatesGroup.search_product.set()
        await bot.send_message(chat_id=message.from_user.id,
                               text='введи продукт')
    await message.delete()


@dp.message_handler(state=MainStatesGroup.search_product)
async def search_products(message: types.Message, state: FSMContext):
    # Находим все продукты, которые содержат искомую строку
    products = BotProductsDB.find_products(message.text)

    # Если список продуктов пуст, отправляем сообщение, что ничего не найдено
    if not products:
        await message.answer("Ничего не найдено")
        return

    async with state.proxy() as data:
        data['current_page'] = 1
        data['pages_count'] = (len(products) - 1) // 50 + 1
        data['products'] = products
    await MainStatesGroup.choose_product.set()
    # Отправляем сообщение с клавиатурой
    await message.answer("Результаты поиска:", reply_markup=search_products_kb(products))


@dp.message_handler(Text(startswith='Далее --> '), state=MainStatesGroup.choose_product)
async def next_page(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['current_page'] += 1
    await message.answer(text="Выберете подходящий вариант:",
                         reply_markup=search_products_kb(data['products'], current_page=data['current_page']))


@dp.message_handler(Text(endswith=' <-- Назад'), state=MainStatesGroup.choose_product)
async def back_page(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['current_page'] -= 1
    await message.answer(text="Выберете подходящий вариант:",
                         reply_markup=search_products_kb(data['products'], current_page=data['current_page']))


@dp.message_handler(state=MainStatesGroup.choose_product)
async def choose_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        for item in data['products']:
            if item['title'].lower() == message.text.lower():
                await message.answer(text=f"{item['title']}\n"
                                          f"{item['proteins']}\n"
                                          f"{item['fats']}\n"
                                          f"{item['carbohydrates']}\n"
                                          f"{item['calories']}",
                                     reply_markup=search_products_kb(data['products'], data['current_page']))

    await MainStatesGroup.search_product.set()
    await message.answer(text="Выберете подходящий вариант:",
                         reply_markup=search_products_kb(data['products'], current_page=data['current_page']))