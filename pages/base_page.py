from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url)

    def click(self, selector: str):
        self.page.locator(selector).click()

    def fill(self, selector: str, text: str):
        self.page.locator(selector).clear()
        self.page.locator(selector).fill(text)

    def get_text(self, selector: str):
        return self.page.inner_text(selector)

    def is_visible(self, selector: str):
        # expect(self.page.locator(selector)).to_be_visible()
        self.page.wait_for_selector(selector)

    def get_attribute(self, selector: str):
        return self.page.locator(selector).get_attribute('aria-label')
