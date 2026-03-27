from logging import getLogger

from playwright.async_api import BrowserContext

log = getLogger(__name__)


async def join_game(
    name: str,
    url: str,
    room_code: str,
    context: BrowserContext,
):
    log.info("Joining game...")
    page = await context.new_page()
    await page.goto(url)
    await page.wait_for_selector("#roomcode")
    await page.fill("#roomcode", room_code)
    await page.fill("#username", name)
    await page.wait_for_selector("#button-join")
    await page.click("#button-join")
    log.info("Joined game.")

    return page
