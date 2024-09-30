import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from utils.config import BASE_URL, USERNAME, PASSWORD


@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    """Fixture to initialize the LoginPage."""
    return LoginPage(page)


@pytest.mark.parametrize("username, password, expected_result", [
    (USERNAME, PASSWORD, True),             # Valid credentials
    (USERNAME, "invalid_pass", False)       # Invalid credentials
])
def test_login(login_page: LoginPage, username: str, password: str, expected_result: bool):
    """Test the login functionality with valid and invalid credentials."""
    login_page.goto(BASE_URL)
    login_page.login(username, password)

    if expected_result:
        # Assert that the user is logged in by checking for the visibility of the navigation panel
        expect(login_page.page.locator('#mega-menu-toggle')).to_be_visible()
    else:
        # Assert that the appropriate error message is displayed
        expect(login_page.page.locator('.css-91zald')).to_contain_text('Invalid username or password')

