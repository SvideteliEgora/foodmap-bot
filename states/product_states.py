from aiogram.dispatcher.filters.state import State, StatesGroup


class ProductsStatesGroup(StatesGroup):
    search_product = State()
    choose_product = State()
    add_product_weight = State()

