from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards import get_menu_kb, get_cancel_kb, get_create_profile_kb
from aiogram.utils.callback_data import CallbackData
import config


bot = Bot(config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Состояние профиля
class ProfileStatesGroup(StatesGroup):

    name = State()
    gender = State()
    age = State()
    weight = State()
    height = State()
    target = State()
    active = State()


# functions
# check weight
def verify_number(number: str) -> bool:
    if not number.isdigit():
        try:
            float(number)

        except ValueError:
            return False

        else:
            return True

    return True


# recommended PFC
def recommended_pfc(weight: float, height: float, age: int, active: str, gender: str, target: str,
                    proteins_percentage=30, fats_percentage=30, carbohydrates_percentage=40) -> int and str:
    activity_coefficient = None
    activity_coefficients_dict = {
        'Минимальный': 1.2,
        'Низкий': 1.375,
        'Средний': 1.55,
        'Высокий': 1.7,
        'Очень высокий': 1.9
    }

    for key, value in activity_coefficients_dict.items():
        if active.startswith(key):
            activity_coefficient = value
            break

    if gender == 'Женский':
        calories = round((655.1 + (9.563 * weight) + (1.85 * height) - (4.676 * age)) * activity_coefficient)
        if target == 'Cнизить вес':
            calories = calories - (calories * 12) // 100

        elif target == 'Набрать вес':
            calories = calories + (calories * 12) // 100
    else:
        calories = round((66.5 + (13.75 * weight) + (5.003 + height) - (6.775 * age)) * activity_coefficient)
        if target == 'Cнизить вес':
            calories = calories - (calories * 15) // 100

        elif target == 'Набрать вес':
            calories = calories + (calories * 15) // 100

    # рассчитываем Б/Ж/У 30/30/40
    proteins = round(((calories * proteins_percentage) // 100) / 4)
    fats = round(((calories * fats_percentage) // 100) / 9)
    carbohydrates = round(((calories * carbohydrates_percentage) // 100) / 4)

    pfc = '{}/{}/{}'.format(proteins, fats, carbohydrates)

    return calories, pfc


@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext) -> None:
    if state is None:
        return

    await state.finish()
    await message.reply('Вы прервали саздание профиля.',
                        reply_markup=get_create_profile_kb())


# хэндлеры
# start
@dp.message_handler(CommandStart())
async def cmd_start(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='Привет добро пожаловать в фуд бот!\n'
                                'Для начала, вам необходимо создать профиль.\n'
                                'Чтобы создать профиль - введите /create и заполните анкету.',
                           reply_markup=get_create_profile_kb())


# create profile - name
@dp.message_handler(commands=['create'])
async def cmd_create(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='Ваше имя:',
                           reply_markup=get_cancel_kb())
    await ProfileStatesGroup.name.set()


# check name
@dp.message_handler(lambda message: not (message.text.isalpha() or len(message.text) >= 15), state=ProfileStatesGroup.name)
async def check_name(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='<em>Некоректные данные</em>\n'
                                'Имя может содержать только букенные символы, в колличестве не больше 15.')


# load name, next gender
@dp.message_handler(state=ProfileStatesGroup.name)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text.title()

    await ProfileStatesGroup.next()
    await bot.send_message(chat_id=message.from_user.id,
                           text="Ваш пол:\n\n"
                                "Введите: <b>'мужской'</b> или <b>'женский'</b>",
                           parse_mode='HTML')


# check gender
@dp.message_handler(lambda message: message.text.lower() not in ['мужской', 'женский'], state=ProfileStatesGroup.gender)
async def check_gender(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text="<em>Некоректные данные.</em>\n\n"
                                "Вам нужно указать свой пол.\n"
                                "Если вы мужчина - введите: <b>'мужской'</b>\n"
                                "Если женщина - введите: <b>'женский'</b>",
                           parse_mode='HTML')


# load gender, next age
@dp.message_handler(Text(equals=['мужской', 'женский'], ignore_case=True), state=ProfileStatesGroup.gender)
async def load_gender(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['gender'] = message.text.title()

    await ProfileStatesGroup.next()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Ваш возраст:')


# check age
@dp.message_handler(lambda message: not message.text.isdigit(), state=ProfileStatesGroup.age)
async def check_age(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='<em>Некоректные данные.</em>\n\n'
                                'Вам нужно указать свой возраст (лет).\n'
                                'Это должно быть <b>целое число</b>, не меньше 8',
                           parse_mode='HTML')


# load age, next weight
@dp.message_handler(state=ProfileStatesGroup.age)
async def load_age(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['age'] = int(message.text)

    await ProfileStatesGroup.next()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Введите ваш вес <em>(кг)</em>:',
                           parse_mode='HTML')


# check weight
@dp.message_handler(lambda message: not verify_number(message.text), state=ProfileStatesGroup.weight)
async def check_weight(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='<em>Некоректные данные</em>\n\n'
                                'Вам нужно указать свой вес <em>(кг)</em>.'
                                'Это должно быть <b>целое (75)</b> или <b>дробное число (75.5)</b>',
                           parse_mode='HTML')


# load weight, next height
@dp.message_handler(state=ProfileStatesGroup.weight)
async def load_weight(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if message.text.isdigit():
            data['weight'] = int(message.text)
        else:
            data['weight'] = round(float(message.text))

    await ProfileStatesGroup.next()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Введите ваш рост <em>(см)</em>:',
                           parse_mode='HTML')


# check height
@dp.message_handler(lambda message: not verify_number(message.text), state=ProfileStatesGroup.height)
async def check_height(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='<em>Некоректные данные</em>\n\n'
                                'Введите ваш рост. Это должно быть <b>целое (75)</b> или <b>дробное число (75.5)</b>',
                           parse_mode='HTML')


# load height, next height
@dp.message_handler(state=ProfileStatesGroup.height)
async def load_height(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if message.text.isdigit():
            data['height'] = int(message.text)
        else:
            data['height'] = round(float(message.text))

    await ProfileStatesGroup.next()
    await bot.send_message(chat_id=message.from_user.id,
                           text="<em>Какая у вас цель?</em>\n\n"
                                "выберете ответ:\n\n"
                                "Снизить вес - введите: <b>'снизить'</b>\n"
                                "Набрать вес - введите: <b>'набрать'</b>\n"
                                "Поддерживать вес - введите: <b>'поддерживать'</b>",
                           parse_mode='HTML')


# check target
@dp.message_handler(lambda message: message.text.lower() not in ['снизить', 'набрать', 'поддерживать'],
                    state=ProfileStatesGroup.target)
async def check_target(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text="<em>Некоректные данные.</em>\n\n"
                                "Укажите цель выбрав нужное утверждение:\n"
                                "Снизить вес - введите: <b>'снизить'</b>\n"
                                "Набрать вес - введите: <b>'набрать'</b>\n"
                                "Поддерживать вес - введите: <b>'поддерживать'</b>",
                           parse_mode='HTML')


# load target, next workout
@dp.message_handler(state=ProfileStatesGroup.target)
async def load_target(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['target'] = f"{message.text.title()} вес"

    await ProfileStatesGroup.next()
    await bot.send_message(chat_id=message.from_user.id,
                           text="Укажите вашу активность:\n\n"
                                "Никаких физических нагрузок - введите <b>'минимальный'</b>\n"
                                "Физические нагрузки 1-3 раза в неделю - введите <b>'низкий'</b>\n"
                                "Физические нагрузки 3-5 раз в неделю- введите <b>'средний'</b>\n"
                                "Физические нагрузки 6-7 раз в неделю- введите <b>'высокий'</b>\n"
                                "Тренировки чаще, чем раз в день- введите <b>'очень высокий'</b>\n",
                           parse_mode='HTML')


# check workout
@dp.message_handler(lambda message: message.text.lower() not in ['минимальный', 'низкий', 'средний', 'высокий', 'очень высокий'],
                    state=ProfileStatesGroup.active)
async def check_target(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text="<em>Некоректные данные.</em>\n\n"
                                "Укажите вашу активность, выбрав подходящее утверждение:\n"
                                "Минимальный (никаких физических нагрузок) - введите <b>'минимальный'</b>\n"
                                "Низкий (физические нагрузки 1-3 раза в неделю)- введите <b>'низкий'</b>\n"
                                "Средний (физические нагрузки 3-5 раз в неделю)- введите <b>'средний'</b>\n"
                                "Высокий (физические нагрузки 6-7 раз в неделю)- введите <b>'высокий'</b>\n"
                                "Очень высокий (тренировки чаще, чем раз в день)- введите <b>'очень высокий'</b>",
                           parse_mode='HTML')


# load workout, finish
@dp.message_handler(state=ProfileStatesGroup.active)
async def load_workout(message: types.Message, state: FSMContext) -> None:
    active_list = ['Минимальный уровень (никаких физических нагрузок)',
                    'Низкий (физические нагрузки 1-3 раза в неделю)',
                    'Средний (физические нагрузки 3-5 раз в неделю)',
                    'Высокий (физические нагрузки 6-7 раз в неделю)',
                    'Очень высокий (тренировки чаще, чем раз в день)',
                    ]
    for item in active_list:
        if item.startswith(message.text.title()):
            async with state.proxy() as data:
                data['active'] = item
                break

    calories, pfc = recommended_pfc(weight=data['weight'], height=data['height'], age=data['age'],
                                    active=data['active'], gender=data['gender'], target=data['target'])

    await state.finish()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Ваш профиль успешно создан!')
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Ваш профиль:\n\n"
                                f"<em>Имя</em>: <b>{data['name']}</b>\n"
                                f"<em>Пол</em>: <b>{data['gender']}</b>\n"
                                f"<em>Возраст</em>: <b>{data['age']} лет</b>\n"
                                f"<em>Вес</em>: <b>{data['weight']} кг</b>\n"
                                f"<em>Рост</em>: <b>{data['height']} см</b>\n"
                                f"<em>Уровень активности</em>: <b>{data['active']}</b>\n"
                                f"<em>Цель</em>: <b>{data['target']}</b>\n\n"
                                f"<em>Ежедневная норма </em>: <b>{calories} ккал</b>\n"
                                f"<em>Ежедневный объем воды</em>: <b>... мл</b>\n"
                                f"<em>Соотношение БЖУ</em>: <b>30/30/40</b>",
                           parse_mode='HTML',
                           reply_markup=get_menu_kb())


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)