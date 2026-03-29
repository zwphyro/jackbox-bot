from src.schemas import BasePromptPayload


class InitialRequest(BasePromptPayload):
    question: str

    def model_dump_prompt(self):
        return f"{self.question}"


class TwistRequest(BasePromptPayload):
    context: str
    question: str
    content_type: str

    def model_dump_prompt(self):
        return f"{self.context}"


class TextVotingOption(BasePromptPayload):
    index: int
    twist: str
    player: str
    player_response: str

    def model_dump_prompt(self):
        return f"index: {self.index}\ntwist: {self.twist}\nplayer: {self.player}\nplayer_response: {self.player_response}"


class TextVoteRequest(BasePromptPayload):
    options: list[TextVotingOption]

    def model_dump_prompt(self):
        return "options:\n" + "\n\n".join(
            "\n".join(["\t" + line for line in option.model_dump_prompt().split("\n")])
            for option in self.options
        )


class ImageChoiceOption(BasePromptPayload):
    index: int
    image_description: str

    def model_dump_prompt(self):
        return f"index: {self.index}\nimage_description: {self.image_description}"


class ImageChoiceRequest(BasePromptPayload):
    question: str
    options: list[ImageChoiceOption]

    def model_dump_prompt(self):
        return f"question: {self.question}\noptions:\n" + "\n\n".join(
            "\n".join(["\t" + line for line in option.model_dump_prompt().split("\n")])
            for option in self.options
        )


class ImageTwistRequest(BasePromptPayload):
    image_description: str
    question: str

    def model_dump_prompt(self):
        return f"image_description: {self.image_description}"


class ImageVotingOption(BasePromptPayload):
    index: int
    image_description: str
    player: str
    twist: str

    def model_dump_prompt(self):
        return f"index: {self.index}\nimage_description: {self.image_description}\nplayer: {self.player}\ntwist: {self.twist}"


class ImageVoteRequest(BasePromptPayload):
    options: list[ImageVotingOption]

    def model_dump_prompt(self):
        return "options:\n" + "\n\n".join(
            "\n".join(["\t" + line for line in option.model_dump_prompt().split("\n")])
            for option in self.options
        )
