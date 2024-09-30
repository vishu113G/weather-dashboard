import pytest
from playwright.sync_api import expect

from pages.dashboard_page import DashboardPage
from pages.data_source_main_page import DataSourcePage


def test_build_dashboard(page, login_and_navigate_to_data_source: DataSourcePage):
    """Test to build the dashboard and verify the panel title."""
    datasource_page = login_and_navigate_to_data_source

    # Add a new data source
    datasource_page.add_data_source()

    # Create the dashboard
    dashboard_page = DashboardPage(page)
    dashboard_page.build_dashboard()

    try:
        expect(page.locator(dashboard_page.panel_title)).to_have_text('Weather data')
    except Exception as e:
        pytest.fail(f"Dashboard could not be created: {str(e)}")
