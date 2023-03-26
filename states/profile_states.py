from aiogram.dispatcher.filters.state import State, StatesGroup


class ProfileStatesGroup(StatesGroup):

    name = State()
    age = State()
    weight = State()
    height = State()
    gender = State()
    target = State()
    active = State()
