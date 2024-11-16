import openai
from config.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class WorkoutService:
    @staticmethod
    async def generate_workout_plan(goal: str, level: str, days_per_week: int) -> str:
        """
        Генерация плана тренировок с использованием OpenAI API
        """
        prompt = f"""
        Составь программу тренировок со следующими параметрами:
        - Цель: {goal}
        - Уровень подготовки: {level}
        - Количество тренировок в неделю: {days_per_week}

        Для каждого упражнения укажи:
        - Название упражнения
        - Количество подходов и повторений
        - Рекомендации по технике
        - Время отдыха между подходами
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
            return f"Ошибка при генерации плана тренировок: {str(e)}" 