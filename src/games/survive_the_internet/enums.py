from enum import StrEnum
from re import sub


class ContentTypeEnum(StrEnum):
    Question = "введи вопрос"
    Location = "введи локацию"
    NameOfPersonOrCharacter = "введи имя личности или персонажа"
    ProductTitle = "введи название товара"
    CrowdfundingCampaignName = "введи название кампании"
    Comment = "введи комментарий"
    NewsHeadline = "введи заголовок новости"
    Hashtag = "введи хештег"
    VideoTitle = "введи название видео"

    def to_readable(self):
        tmp = sub("(.)([A-Z][a-z]+)", r"\1 \2", self.name)
        return sub("([a-z0-9])([A-Z])", r"\1 \2", tmp).lower()
