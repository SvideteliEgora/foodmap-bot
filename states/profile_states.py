from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateProfileStatesGroup(StatesGroup):

    name = State()
    age = State()
    weight = State()
    height = State()
    gender = State()
    target = State()
    active = State()


class EditProfileStatesGroup(StatesGroup):

    name = State()
    age = State()
    weight = State()
    height = State()
    gender = State()
    target = State()
    active = State()
    daily_calories = State()
    daily_water_allowance = State()
    bzhu = State()