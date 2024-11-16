import openai
from config.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class NutritionService:
    @staticmethod
    async def generate_meal_plan(calories: float, goal: str) -> str:
        """
        Генерация плана питания с использованием OpenAI API
        """
        prompt = f"""
        Составь план питания на день с учетом следующих параметров:
        - Целевые калории: {calories} ккал
        - Цель: {goal}
        
        План должен включать:
        1. Завтрак
        2. Перекус
        3. Обед
        4. Полдник
        5. Ужин
        
        Для каждого приема пищи укажи:
        - Блюда
        - Калории
        - Белки/Жиры/Углеводы
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Ошибка при генерации плана питания: {str(e)}" 