import pytest

from pages.dashboard_page import DashboardPage
from pages.data_source_main_page import DataSourcePage
from utils.common_utils import *
from utils.config import *


def test_configure_data_source(page, login_and_navigate_to_data_source: DataSourcePage):
    """Test to configure a data source and validate the dashboard build process."""
    datasource_page = login_and_navigate_to_data_source

    # Add a new data source
    datasource_page.add_data_source()

    # Build the dashboard for the data source
    dashboard_page = DashboardPage(page)
    dashboard_page.build_dashboard()

    # Taking a screenshot of the created dashboard
    try:
        page.locator(dashboard_page.dashboard_panel).screenshot(path=TEST_DASHBOARD)
    except Exception as e:
        pytest.fail(f"Failed to take screenshot: {e}")

    # Compare the screenshots
    assert compare_images(TEST_DASHBOARD, REFERENCE_DASHBOARD), (
        f"Dashboard screenshot differs from reference at {TEST_DASHBOARD}"
    )


