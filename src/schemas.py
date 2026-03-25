from pydantic import BaseModel


class InitialRequest(BaseModel):
    question: str


class TwistRequest(BaseModel):
    context: str
    question: str


class TextVotingOption(BaseModel):
    index: int
    twist: str
    player: str
    player_response: str


class TextVoteRequest(BaseModel):
    options: list[TextVotingOption]


class ImageChoiceOption(BaseModel):
    index: int
    image_description: str


class ImageChoiceRequest(BaseModel):
    question: str
    options: list[ImageChoiceOption]


class ImageTwistRequest(BaseModel):
    image_description: str
    question: str


class ImageVotingOption(BaseModel):
    index: int
    image_description: str
    player: str
    twist: str


class ImageVoteRequest(BaseModel):
    options: list[ImageVotingOption]
