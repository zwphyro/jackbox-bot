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
    log.info("Waiting for game to load.")
    await page.wait_for_selector("#roomcode")
    log.info("filling room code.")
    await page.fill("#roomcode", room_code)
    log.info("Filled room code.")
    await page.fill("#username", name)
    log.info("Filled username.")
    await page.wait_for_selector("#button-join")
    log.info("Waiting for join button.")
    await page.click("#button-join")
    log.info("Joined game.")

    return page
