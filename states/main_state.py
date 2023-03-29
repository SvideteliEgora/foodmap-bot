from aiogram.dispatcher.filters.state import State, StatesGroup


class MainStatesGroup(StatesGroup):
    search_product = State()
    choose_product = State()
