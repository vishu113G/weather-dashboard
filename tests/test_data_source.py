import pytest
from playwright.sync_api import expect

from pages.data_source_main_page import DataSourcePage


def test_configure_data_source(page, login_and_navigate_to_data_source: DataSourcePage):
    """Test to configure a data source and validate the process."""
    datasource_page = login_and_navigate_to_data_source

    # Add a new data source
    datasource_page.add_data_source()
    try:
        expect(page.locator(datasource_page.connection_success_toast)).to_be_visible()
    except Exception as e:
        pytest.fail(f"Could not connect to the Data source: {str(e)}")


