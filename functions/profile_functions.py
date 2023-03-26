# check weight, height
def verify_number(number: str) -> bool:
    if not number.isdigit():
        try:
            float(number)

        except ValueError:
            return False

        else:
            return True

    return True


# bzhu
def get_calculate_bzhu(weight: float, height: float, age: int, active: str, gender: str, target: str,
                       proteins_percentage=30, fats_percentage=30, carbohydrates_percentage=40) -> int and str:
    activity_coefficient = None
    activity_coefficients_dict = {
        'Никаких физических нагрузок': 1.2,
        'Физические нагрузки 1-3 раза в неделю': 1.375,
        'Физические нагрузки 3-5 раз в неделю': 1.55,
        'Физические нагрузки 6-7 раз в неделю': 1.7,
        'Тренировки чаще, чем раз в день': 1.9
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

    bzhu = '{}/{}/{}'.format(proteins, fats, carbohydrates)

    return calories, bzhu