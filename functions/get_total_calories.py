
def total_product_value(product_id, product_title, protein, fats, carbohydrates, calories, total_weight) -> dict:
    """Находим общую калорийность продукта"""
    calories = float(calories)
    total_weight = int(total_weight)
    protein = int(protein)
    fats = float(fats)
    carbohydrates = float(carbohydrates)

    total_calories = round(calories / 100 * total_weight)

    """Находим общий белок продукта"""
    total_proteins = round(protein / 100 * total_weight)

    """Находим общее количество жиров продукта"""
    total_fats = round(fats / 100 * total_weight)

    """Находим общее количество углеводов продукта"""
    total_carbohydrates = round(carbohydrates / 100 * total_weight)

    product_data = {
        'id': product_id,
        'title': product_title,
        'calories': total_calories,
        'proteins': total_proteins,
        'fats': total_fats,
        'carbohydrates': total_carbohydrates,
        'weight': total_weight
    }

    return product_data


