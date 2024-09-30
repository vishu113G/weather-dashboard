from playwright.sync_api import expect

from pages.base_page import BasePage
from utils.config import DATA_SOURCE_NAME, MYSQL_HOST, MYSQL_DATABASE, MYSQL_USERNAME, MYSQL_PASSWORD


class DataSourceMySqlPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.mysql_title = '.css-1l9jgkm'
        self.name_input = '#basic-settings-name'

        self.host_input = '[name="host"]'
        self.database_input = '[name="database"]'
        self.username_input = '[placeholder="Username"]'
        self.password_input = '[type="password"]'
        self.save_button = '[type="submit"]'

        self.connection_error_toast = '[data-testid*="error"]'
        self.connection_success_toast = '[data-testid*="success"]'
        self.build_dashboard_link = '[aria-label="Create a dashboard"]'

    def configure_data_source(self):
        """
        Configures the MySQL data source in Grafana using values from the config.
        """
        try:
            # Wait for the MySQL data source page to load
            expect(self.page.locator(self.mysql_title)).to_be_visible(timeout=5000)

            # Fill the form fields using values from config.py
            self.fill(self.name_input, DATA_SOURCE_NAME)
            self.fill(self.host_input, MYSQL_HOST)
            self.fill(self.database_input, MYSQL_DATABASE)
            self.fill(self.username_input, MYSQL_USERNAME)
            self.fill(self.password_input, MYSQL_PASSWORD)

            # Click the save button
            self.click(self.save_button)

            # Wait for success or error toast
            if self.page.locator(self.connection_success_toast).is_visible():
                print(f"Data source '{DATA_SOURCE_NAME}' configured successfully.")
            elif self.page.locator(self.connection_error_toast).is_visible():
                error_message = self.page.locator(self.connection_error_toast).inner_text()
                raise RuntimeError(f"Failed to configure data source: {error_message}")

        except Exception as e:
            raise RuntimeError(f"Error during MySQL data source configuration: {str(e)}")

