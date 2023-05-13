from loader import dp, bot, UserFeedingDB, UserProfilesDB, ProductsDB
from aiogram import types
from murkups.profile_markups import CREATE_PROFILE
from datetime import date
from aiogram.types import ParseMode
from murkups.main_murkups import ikb_main, IKB_ADD_PRODUCT
from functions.profile_functions import calculate_daily_pfc
from functions.get_total_calories import total_product_value
from states.main_states import MainStatesGroup
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=['main'])
async def cmd_main(message: types.Message, state: FSMContext) -> None:

    # Получаем ежедневное БЖУ пользователя в словаре
    user_daily_pfc = UserProfilesDB.get_daily_pfc(message.from_user.id)

    if not UserProfilesDB.user_exists(user_id=message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text='У тебя еще нет профиля, предлагаю создать его.',
                               reply_markup=CREATE_PROFILE)
        return

    if not UserFeedingDB.get_feeding_today(message.from_user.id):
        await MainStatesGroup.main.set()
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'<i>Ваш текущий вес</i>: <b>{UserProfilesDB.get_one_user_param(user_id=message.from_user.id, column="weight")} kg</b>\n\n'
                                    f'<i>Дата</i>: <b>{date.today()}</b>\n\n\n'
                                    f'<i>Сегодня вы не добавили ни одного продукта</i>\n\n\n'
                                    f'<i>ИТОГО</i>:\n'
                                    f'                  (<i>Б/Ж/У</i>)    <b>0/{user_daily_pfc.get("p")} 0/{user_daily_pfc.get("f")} 0/{user_daily_pfc.get("c")}</b>\n'
                                    f'                  (<i>Ккал</i>)      <b>0/1555</b>\n'
                                    f'                  (<i>Вода</i>)      <b>1455 ml</b>',
                               parse_mode=ParseMode.HTML,
                               reply_markup=IKB_ADD_PRODUCT)
    else:
        # Питание пользователя за сегодня
        feeding_today = UserFeedingDB.get_feeding_today(user_id=message.from_user.id)

        product_lines = []

        count_proteins = 0
        count_fats = 0
        count_carbohydrates = 0
        count_calories = 0
        products = []
        feeding_products_data = []

        for data in feeding_today:
            product_id = data.get('product_id')
            feeding_time = data.get('feeding_time')
            product_weight = data.get('product_weight')
            feeding_id = data.get('id')

            # Находим продукт в БД
            product = ProductsDB.get_product(product_id)

            title = product.get('title')
            proteins = product.get('proteins')
            fats = product.get('fats')
            carbohydrates = product.get('carbohydrates')
            calories = product.get('calories')

            eaten_product = total_product_value(product_id, title, proteins, fats, carbohydrates, calories, product_weight)

            count_proteins += eaten_product.get('proteins')
            count_fats += eaten_product.get('fats')
            count_carbohydrates += eaten_product.get('carbohydrates')
            count_calories += eaten_product.get('calories')

            product_text = f"{feeding_time}   {eaten_product.get('title')}, {eaten_product.get('weight')} г\n" \
                           f"                   Б/Ж/У:   {eaten_product.get('proteins')}/{eaten_product.get('fats')}/{eaten_product.get('carbohydrates')}\n" \
                           f"                   Ккал:    {eaten_product.get('calories')}"

            products.append({feeding_id: product_text})

            product_lines.append(product_text)

            feeding_products_data.append({
                'feeding_id': feeding_id,
                'product_title': title,
                'product_weight': product_weight,
                'feeding_time': feeding_time,
            })

        feeding_products_today = "\n\n".join(product_lines[:5])

        user_weight = UserProfilesDB.get_one_user_param(message.from_user.id, 'weight')
        daily_calories = UserProfilesDB.get_one_user_param(message.from_user.id, 'daily_calories')
        daily_pfc = UserProfilesDB.get_daily_pfc(message.from_user.id)

        await MainStatesGroup.main.set()
        async with state.proxy() as data:
            data['current_page'] = 1
            data['feeding_products_data'] = feeding_products_data
            data['feeding_products'] = product_lines
            data['products_on_page'] = 5
            data['user_weight'] = user_weight
            data['date'] = date.today()
            data['count_proteins'] = count_proteins
            data['daily_proteins'] = daily_pfc.get("p")
            data['count_fats'] = count_fats
            data['daily_fats'] = daily_pfc.get("f")
            data['count_carbohydrates'] = count_carbohydrates
            data['daily_carbohydrates'] = daily_pfc.get("c")
            data['count_calories'] = count_calories
            data['daily_calories'] = daily_calories

        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Ваш текущий вес: {user_weight} кг\n\n'
                                    f'Дата: {date.today()}\n\n'
                                    f'{feeding_products_today}\n\n'
                                    f'ИТОГО:        Б/Ж/У - {count_proteins}/{daily_pfc.get("p")} {count_fats}/{daily_pfc.get("f")} {count_carbohydrates}/{daily_pfc.get("c")}\n'
                                    f'                      Ккал - {count_calories}/{daily_calories}\n'
                                    f'                      Вода - 2150 мл',
                               parse_mode=ParseMode.HTML,
                               reply_markup=ikb_main(products))








