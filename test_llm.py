import asyncio
from openai import AsyncOpenAI

from src.llm_service import LLMService
from src.schemas import InitialRequest, TwistRequest
from src.logging import configure_logging
from src.settings import get_settings

configure_logging()


async def twist_response_test(llm_service: LLMService):
    contexts = [
        "5 минут",
        "Вкусно, но не более",
        "Он меня пугает если честно",
        "Обожаю, никак не могу отлипнуть",
        "Еще чего",
        "Приятно",
        "Скучно",
        "Тут как получится, не всегда все хорошо",
        "У него смешная одежда",
    ]

    content_type_map = {
        "вопрос": "question",
        "локацию": "location",
        "имя личности или персонажа": "name of person or character",
        "название товара": "product name",
        "название кампании": "crowdfunding campaign name",
        "комментарий": "comment",
        "заголовок новости": "news headline",
        "хештег": "hashtag",
        "название видео": "video title",
    }

    content_types = [
        "вопрос",
        "локацию",
        "имя личности или персонажа",
        "название товара",
        "название кампании",
        "комментарий",
        "заголовок новости",
        "хештег",
        "название видео",
    ]

    questions = [
        "будет смешным ответом на этот вопрос:",
        "будет смешным комментарием к чекину в этой локации:",
        "будет смешной рекомендацией на этого человека:",
        "будет смешным отзывом на этот товар:",
        "будет смешным комментарием к компании под сбором денег под названием:",
        "будет смешным ответом на этот комментарий:",
        "будет ужасным комментарием под этой новостью:",
        "Будет более смешным с хэштегом:",
        "будет смешным комментарием к видео с названием:",
    ]

    for context, question, content_type in zip(contexts, questions, content_types):
        print(
            await llm_service.generate_text_twist(
                TwistRequest(
                    context=context, question=question, content_type=content_type
                )
            )
        )


async def initial_response_test(llm_service: LLMService):
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


async def main():
    client = AsyncOpenAI(
        base_url=get_settings().llm_base_url,
        api_key=get_settings().llm_api_key,
    )
    llm_service = LLMService(client, get_settings().llm_model)
    await twist_response_test(llm_service)


if __name__ == "__main__":
    asyncio.run(main())
