from abc import ABC

from playwright.async_api import Page


class BaseRepository(ABC):
    def __init__(self, page: Page, timeout: int):
        self._page = page
        self._page.set_default_timeout(timeout)
