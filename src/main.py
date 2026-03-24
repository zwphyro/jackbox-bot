import asyncio
from playwright.async_api import Page, async_playwright


async def handle_image_question_phase(page: Page):
    question_locator = page.locator(
        ".blackBox",
    )
    await question_locator.wait_for(state="visible", timeout=5 * 60 * 1000)

    question_text = await question_locator.inner_text()
    print(question_text)

    choices_container = page.locator(
        "#choicesRegion > div > *",
    )
    await choices_container.first.wait_for(state="visible", timeout=5 * 60 * 1000)

    options = await choices_container.all()
    choices_data = [
        {
            "index": index,
            "response": await option.locator("button").inner_text(),
            "locator": option,
        }
        for index, option in enumerate(options)
    ]

    print([f"{x['index']}: {x['response']}" for x in choices_data])

    if choices_data:
        best_choice = max(choices_data, key=lambda x: len(x["response"]))
        await best_choice["locator"].click()
    else:
        pass

    finalImage = page.locator(".finalRoundImage")
    await finalImage.wait_for(state="visible", timeout=5 * 60 * 1000)

    image_description = await finalImage.get_attribute("aria-label")
    prompt_text = await page.locator(".belowBlackBox").inner_text()
    print(image_description, prompt_text)

    await page.fill("#input-text-textarea", "Смешной заголовок к этому")
    await page.click("#buttons > div > div > button")


async def handle_text_question_phase(page: Page):
    question_locator = page.locator(
        ".belowBlackBox",
    )
    await question_locator.wait_for(state="visible", timeout=5 * 60 * 1000)

    question_text = await question_locator.inner_text()

    await page.fill("#input-text-textarea", "Мой первый ответ")
    await page.click("#buttons > div > div > button")

    black_box = page.locator(".blackBox")
    await black_box.wait_for(state="visible", timeout=5 * 60 * 1000)

    other_user_context = await black_box.inner_text()
    prompt_text = await page.locator(".belowBlackBox").inner_text()

    await page.fill("#input-text-textarea", "Смешной заголовок к этому")
    await page.click("#buttons > div > div > button")


async def handle_image_voting_phase(page: Page):
    choices_container = page.locator("#choicesRegion > div > *")
    await choices_container.first.wait_for(state="visible", timeout=5 * 60 * 1000)

    options = await choices_container.all()
    choices_data = [
        {
            "index": index,
            "image_description": await option.locator(".voteThumbnail").inner_text(),
            "player": await option.locator(".votePlayer").inner_text(),
            "response": await option.locator(".voteResponse").inner_text(),
            "locator": option,
        }
        for index, option in enumerate(options)
    ]

    print(
        [
            f"{x['index']}: {x['image_description']}, {x['player']}: {x['response']}"
            for x in choices_data
        ]
    )

    if choices_data:
        best_choice = max(choices_data, key=lambda x: len(x["response"]))
        await best_choice["locator"].click()
    else:
        pass


async def handle_text_voting_phase(page: Page):
    choices_container = page.locator("#choicesRegion > div > *")
    await choices_container.first.wait_for(state="visible", timeout=5 * 60 * 1000)

    options = await choices_container.all()
    choices_data = [
        {
            "index": index,
            "header": await option.locator(".voteTwistHeader").inner_text(),
            "player": await option.locator(".votePlayer").inner_text(),
            "response": await option.locator(".voteResponse").inner_text(),
            "locator": option,
        }
        for index, option in enumerate(options)
    ]

    if choices_data:
        best_choice = max(choices_data, key=lambda x: len(x["response"]))
        await best_choice["locator"].click()
    else:
        pass


async def play_survive_the_internet(page: Page):
    for _ in range(3):
        await handle_text_question_phase(page)
        await handle_text_voting_phase(page)

    await handle_image_question_phase(page)
    await handle_image_voting_phase(page)


async def run_jackbox_bot(room_code, bot_name):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://jackbox.fun/")
        await page.wait_for_selector("#roomcode")
        await page.fill("#roomcode", room_code)
        await page.fill("#username", bot_name)
        await page.click("#button-join")
        await page.wait_for_timeout(3000)

        await play_survive_the_internet(page)

        await browser.close()


if __name__ == "__main__":
    ROOM_CODE = "biqi"
    BOT_NAME = "RoboJoke"

    asyncio.run(run_jackbox_bot(ROOM_CODE, BOT_NAME))
