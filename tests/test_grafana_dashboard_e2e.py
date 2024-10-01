import pytest

from pages.dashboard_page import DashboardPage
from pages.data_source_main_page import DataSourcePage
from utils.common_utils import *
from utils.config import *


def test_grafana_dashboard_e2e(page, login_and_navigate_to_data_source: DataSourcePage, load_data_in_db: int):
    """Test to load data in a table, configure a data source and validate the dashboard build process."""

    csv_row_count, db_row_count = load_data_in_db
    # Assert records in the DB are the same as present in the file used for loading data
    assert csv_row_count == db_row_count, (
        f"Row count mismatch: CSV has {csv_row_count} rows, but DB has {db_row_count} records."
    )

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


