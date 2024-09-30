from playwright.sync_api import expect

from pages.base_page import BasePage
from utils.config import *


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.login_container = '.login-content-box'
        self.username_input = '[name="user"]'
        self.password_input = '[name="password"]'
        self.submit_button = '[type="submit"]'

        self.menu_button = '#mega-menu-toggle'

    def login(self, username=USERNAME, password=PASSWORD):
        """Log in to the application using the provided username and password."""

        # Wait for the login container to be visible
        expect(self.page.locator(self.login_container)).to_be_visible(timeout=5000)

        # Fill in the username and password fields
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)

        # Click the submit button
        self.click(self.submit_button)

        # Assertions/Expect statements in login scenarios will be covered by tests to handle invalid login scenarios


