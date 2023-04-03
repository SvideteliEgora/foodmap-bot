from loader import dp, bot, UserFeedingDB, UserProfilesDB, ProductsDB
from aiogram import types
from murkups.profile_markups import CREATE_PROFILE
from datetime import date
from aiogram.types import ParseMode
from murkups.main_murkups import ADD_OR_DELETE_PRODUCT_IKB
from functions.profile_functions import calculate_daily_pfc
from functions.get_total_calories import total_product_value


@dp.message_handler(commands=['main'])
async def cmd_main(message: types.Message) -> None:

    # Получаем ежедневное БЖУ пользователя в словаре
    user_daily_pfc = UserProfilesDB.get_daily_pfc(message.from_user.id)

    if not UserProfilesDB.user_exists(user_id=message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text='У тебя еще нет профиля, предлагаю создать его.',
                               reply_markup=CREATE_PROFILE)
        return

    if not UserFeedingDB.get_feeding_today(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'<u><i>Ваш текущий вес</i></u>: <b>{UserProfilesDB.get_one_user_param(user_id=message.from_user.id, column="weight")} kg</b>\n\n'
                                    f'<u><i>Дата</i></u>: <b>{date.today()}</b>\n\n\n'
                                    f'<i><s>Сегодня вы не добавили ни одного продукта</s></i>\n\n\n'
                                    f'<u><i>ИТОГО</i></u>:\n'
                                    f'                  (<i>Б/Ж/У</i>)    <b>0/{user_daily_pfc.get("p")} 0/{user_daily_pfc.get("f")} 0/{user_daily_pfc.get("c")}</b>\n'
                                    f'                  (<i>Ккал</i>)      <b>0/1555</b>\n'
                                    f'                  (<i>Вода</i>)      <b>1455 ml</b>',
                               parse_mode=ParseMode.HTML,
                               reply_markup=ADD_OR_DELETE_PRODUCT_IKB)
    else:
        # Питание пользователя за сегодня
        feeding_today = UserFeedingDB.get_feeding_today(user_id=message.from_user.id)

        product_lines = []

        count_proteins = 0
        count_fats = 0
        count_carbohydrates = 0
        count_calories = 0

        for data in feeding_today:
            product_id = data.get('product_id')
            feeding_time = data.get('feeding_time')
            product_weight = data.get('product_weight')

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

            product_lines.append(f"{feeding_time}   {eaten_product.get('title')}, {eaten_product.get('weight')} г\n"
                                 f"                   Б/Ж/У:   {eaten_product.get('proteins')}/{eaten_product.get('fats')}/{eaten_product.get('carbohydrates')}\n"
                                 f"                   Ккал:    {eaten_product.get('calories')}")

        product_text = "\n\n".join(product_lines)

        user_weight = UserProfilesDB.get_one_user_param(message.from_user.id, 'weight')
        daily_calories = UserProfilesDB.get_one_user_param(message.from_user.id, 'daily_calories')
        daily_pfc = UserProfilesDB.get_daily_pfc(message.from_user.id)

        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Ваш текущий вес: {user_weight} кг\n\n'
                                    f'Дата: {date.today()}\n\n'
                                    f'{product_text}\n\n'
                                    f'ИТОГО:        Б/Ж/У - {count_proteins}/{daily_pfc.get("p")} {count_fats}/{daily_pfc.get("f")} {count_carbohydrates}/{daily_pfc.get("c")}\n'
                                    f'                      Ккал - {count_calories}/{daily_calories}\n'
                                    f'                      Вода - 2150 мл',
                               parse_mode=ParseMode.HTML,
                               reply_markup=ADD_OR_DELETE_PRODUCT_IKB)







