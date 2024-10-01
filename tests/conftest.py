import os

import pytest
from playwright.sync_api import expect

from pages.data_source_main_page import DataSourcePage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.config import BASE_URL, USERNAME, PASSWORD
from utils.db_utils import create_db_connection, close_db_connection, create_table_in_database, insert_data_from_csv, fetch_rows_count


@pytest.fixture(scope="function")
def load_data_in_db(page):
    conn = create_db_connection()
    cur = conn.cursor()
    create_table_in_database(cur)
    current_dir = os.path.dirname(__file__)
    csv_file_path = os.path.join(current_dir, 'test_data', 'weather_data.csv')
    try:
        with conn.cursor() as cur:
            # Insert data and get row count from CSV
            csv_row_count = insert_data_from_csv(cur, csv_file_path)

            # Commit changes
            conn.commit()

            # Get number of records from the DB
            db_row_count = fetch_rows_count(cur)

    except Exception as e:
        pytest.fail(f"Database operation failed: {e}")
    yield csv_row_count, db_row_count
    close_db_connection(conn)  # Cleanup: Close the database connection after the test is done


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
