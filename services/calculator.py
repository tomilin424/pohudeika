def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
    """
    Расчет базового метаболизма по формуле Миффлина-Сан Жеора
    """
    if gender.lower() == "мужской":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    return round(bmr, 2)

def calculate_daily_calories(bmr: float, activity_level: str, goal: str) -> float:
    """
    Расчет суточной нормы калорий с учетом активности и цели
    """
    activity_multipliers = {
        "низкая": 1.2,
        "умеренная": 1.375,
        "средняя": 1.55,
        "высокая": 1.725,
        "очень высокая": 1.9
    }
    
    maintenance_calories = bmr * activity_multipliers[activity_level]
    
    if goal == "похудение":
        return round(maintenance_calories - 500, 2)
    elif goal == "набор массы":
        return round(maintenance_calories + 300, 2)
    else:
        return round(maintenance_calories, 2) 