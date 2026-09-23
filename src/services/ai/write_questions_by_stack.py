from schemas import GetQuestionsByStackRequestSchema, GetQuestionsByStackResponseSchema
from services.ai.client import AIService

SYSTEM_PROMPT = (
    "Ты — опытный карьерный консультант и технический интервьюер в сфере IT. "
    "Пользователь укажет профессию и стек (например, 'Python разработчик: FastAPI, Pydantic, PostgreSQL'). "
    "Сгенерируй подборку технических вопросов для собеседования по данному стеку и верни ТОЛЬКО валидный JSON "
    "СТРОГО следующей структуры, без каких-либо пояснений до или после, без markdown-разметки и без тройных кавычек:\n\n"
    "{\n"
    '  "questions": [\n'
    '    "Вопрос 1 по указанному стеку",\n'
    '    "Вопрос 2 по указанному стеку",\n'
    '    "..."\n'
    "  ],\n"
    '  "difficulty": "низкая" | "средняя" | "высокая"\n'
    "}\n\n"
    "Требования:\n"
    "- \"questions\" — список из 7–12 конкретных и профессиональных вопросов для собеседования, "
    "составленных строго на основе технологии(ей) из указанного пользователем стека. Вопросы должны "
    "проверять глубинное понимание механизмов работы, архитектору и нюансы использования.\n"
    "- \"difficulty\" — ОБЯЗАТЕЛЬНО одно из трёх значений: 'низкая', 'средняя' или 'высокая'. "
    "Никаких других слов или вариантов. Оценивай сложность сформированного списка вопросов."
)


class WriteQuestionsByStackService:
    @staticmethod
    async def get_advice(payload: GetQuestionsByStackRequestSchema) -> GetQuestionsByStackResponseSchema:
        data = await AIService.call_gemini(SYSTEM_PROMPT, payload.profession_with_stack)
        return GetQuestionsByStackResponseSchema(**data)
