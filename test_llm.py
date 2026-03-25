import asyncio
from openai import AsyncOpenAI

from src.llm_service import LLMService
from src.schemas import InitialRequest


async def main(llm_base_url: str, llm_api_key: str, llm_model: str):
    client = AsyncOpenAI(base_url=llm_base_url, api_key=llm_api_key)
    llm_service = LLMService(client, llm_model)

    questions = [
        "Коротко опишите, какие качества должны быть у шеф-повара.",
        "Коротко опишите последнего человека, в которого вы влюблялись.",
        "Как бы вы описали Гарри Поттера?",
        "Что бы тебе хотелось сказать себе несколько лет назад?",
        "Почему Мона Лиза так популярна?",
        "Что объединяет всех тех кто занимается йогой?",
        "Что у вас общего с твоей мамой?",
        "Что ты хочешь сказать тому, кто резко встаёт у тебя на пути?",
        "Какую роль ты играешь в своей семье?",
    ]

    for question in questions:
        print(
            await llm_service.generate_initial_response(
                InitialRequest(question=question)
            )
        )


if __name__ == "__main__":
    OPENAI_BASE_URL = "https://router.huggingface.co/v1"
    OPENAI_API_KEY = ""
    OPENAI_MODEL = "deepseek-ai/DeepSeek-V3.1"

    asyncio.run(main(OPENAI_BASE_URL, OPENAI_API_KEY, OPENAI_MODEL))
