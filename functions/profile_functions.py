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


def calculate_daily_calories(weight: float, height: float, age: int, active: str, gender: str, target: str) -> int:
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
        calories = round((66.5 + (13.75 * weight) + (5.003 * height) - (6.775 * age)) * activity_coefficient)
        if target == 'Cнизить вес':
            calories = calories - (calories * 15) // 100

        elif target == 'Набрать вес':
            calories = calories + (calories * 15) // 100

    return calories


def calculate_daily_pfc(calories: float, pfc_ratio: dict) -> dict:

    daily_pfc_dict = {
        'proteins': round(((calories * pfc_ratio.get('proteins')) // 100) / 4),
        'fats': round(((calories * pfc_ratio.get('fats')) // 100) / 9),
        'carbohydrates': round(((calories * pfc_ratio.get('carbohydrates')) // 100) / 4)
    }

    daily_pfc_string = '{}/{}/{}'.format(daily_pfc_dict.get('proteins'), daily_pfc_dict.get('fats'), daily_pfc_dict.get('carbohydrates'))

    pfc_full_stack = {
        'daily_pfc_dict': daily_pfc_dict,
        'daily_pfc_string': daily_pfc_string
    }

    return pfc_full_stack


def calculate_daily_water_allowance(weight: float) -> int:
    daily_water_allowance = round(weight * 30)

    return daily_water_allowance
