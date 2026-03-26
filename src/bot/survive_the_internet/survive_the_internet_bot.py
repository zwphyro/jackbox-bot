from logging import getLogger

from src.bot.survive_the_internet.survive_the_internet_repository import (
    SurviveTheInternetRepository,
)
from src.llm_service import LLMService
from src.schemas import (
    ImageChoiceRequest,
    ImageTwistRequest,
    ImageVoteRequest,
    InitialRequest,
    TextVoteRequest,
    TwistRequest,
)

log = getLogger(__name__)


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


class SurviveTheInternetBot:
    def __init__(
        self, repository: SurviveTheInternetRepository, llm_service: LLMService
    ):
        self._repository = repository
        self._llm_service = llm_service

    @property
    def queue(self):
        return [
            self.initial_response,
            self.twist_response,
            self.text_voting,
            self.initial_response,
            self.twist_response,
            self.text_voting,
            self.initial_response,
            self.twist_response,
            self.text_voting,
            self.image_choice,
            self.image_twist,
            self.image_voting,
        ]

    async def initial_response(self):
        log.info("Executing phase: Initial Response")
        question = await self._repository.get_question()

        payload = InitialRequest(question=question)
        response = await self._llm_service.generate_initial_response(payload)

        await self._repository.submit_response(response)
        log.info("Initial Response phase completed.")

    async def twist_response(self):
        log.info("Executing phase: Twist Response")
        context = await self._repository.get_context()
        question = await self._repository.get_question()
        content_type = await self._repository.get_content_type()

        payload = TwistRequest(
            context=context,
            question=question,
            content_type=content_type_map.get(content_type) or content_type,
        )
        answer = await self._llm_service.generate_text_twist(payload)

        await self._repository.submit_response(answer)
        log.info("Twist Response phase completed.")

    async def text_voting(self):
        log.info("Executing phase: Text Voting")
        options = await self._repository.get_text_voting_options()

        payload = TextVoteRequest(options=options)
        selected_index = await self._llm_service.choose_text_vote(payload)

        if 0 <= selected_index < len(options):
            await self._repository.select_option(selected_index)
            log.info(f"Clicked option {selected_index} for Text Voting.")
        else:
            await self._repository.select_option(0)
            log.warning("Invalid index returned. Clicked option 0 fallback.")

    async def image_choice(self):
        log.info("Executing phase: Image Choice")
        question = await self._repository.get_context()

        options = await self._repository.get_image_options()

        payload = ImageChoiceRequest(question=question, options=options)
        selected_index = await self._llm_service.choose_image(payload)

        if 0 <= selected_index < len(options):
            await self._repository.select_option(selected_index)
            log.info(f"Clicked option {selected_index} for Image Choice.")
        else:
            await self._repository.select_option(0)
            log.warning("Invalid index returned. Clicked option 0 fallback.")

    async def image_twist(self):
        log.info("Executing phase: Image Twist Comment")
        image_description = await self._repository.get_image_description()
        prompt_text = await self._repository.get_question()

        payload = ImageTwistRequest(
            image_description=image_description, question=prompt_text
        )
        answer = await self._llm_service.generate_image_twist(payload)

        await self._repository.submit_response(answer)
        log.info("Image Twist phase completed.")

    async def image_voting(self):
        log.info("Executing phase: Image Voting")
        options = await self._repository.get_image_voting_options()

        payload = ImageVoteRequest(options=options)
        selected_index = await self._llm_service.choose_image_vote(payload)

        if 0 <= selected_index < len(options):
            await self._repository.select_option(selected_index)
            log.info(f"Clicked option {selected_index} for Image Voting.")
        else:
            await self._repository.select_option(selected_index)
            log.warning("Invalid index returned. Clicked option 0 fallback.")
