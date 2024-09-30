import pytest
from playwright.sync_api import expect

from pages.data_source_main_page import DataSourcePage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.config import BASE_URL, USERNAME, PASSWORD


@pytest.fixture(scope="function")
def login_and_navigate_to_data_source(page):
    """Fixture to log in and navigate to the DataSource page."""
    login_page = LoginPage(page)
    login_page.goto(BASE_URL)
    login_page.login(USERNAME, PASSWORD)
    home_page = HomePage(page)
    expect(page.locator(home_page.menu_button)).to_be_visible()  # Check for successful login
    home_page.open_data_source()
    datasource_page = DataSourcePage(page)
    yield datasource_page
    datasource_page.delete_created_data_source()
