from playwright.sync_api import expect

from pages.base_page import BasePage
from pages.data_source_mysql_page import DataSourceMySqlPage
from pages.home_page import HomePage


class DataSourcePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.data_sources_title = '[title="Data sources"]'
        self.add_data_source_button = '[href*="datasources/new"]'
        self.data_sources_input = '[placeholder*="Filter by name"]'
        self.mysql_data_source_button = 'button[aria-label*="MySQL"]' \
                                        ''
        self.edit_data_source_button = '[href*="datasources/edit"]'
        self.delete_data_source_button = '[data-testid*="Delete"]'
        self.confirm_delete_button = '[data-testid*="Confirm"]'
        self.confirm_delete_toast = '.css-i7txp7'

        self.connection_error_toast = '[data-testid*="error"]'
        self.connection_success_toast = '[data-testid*="success"]'

    def add_data_source(self, data_source_name='mysql'):
        """Add a new data source with the given name."""
        self.click(self.add_data_source_button)
        self.fill(self.data_sources_input, data_source_name)
        self.click(self.mysql_data_source_button)
        data_source_mysql_page = DataSourceMySqlPage(self.page)
        data_source_mysql_page.configure_data_source()

    def delete_created_data_source(self):
        """Delete the created data source."""
        try:
            home_page = HomePage(self.page)
            home_page.open_data_source()
            self.click(self.edit_data_source_button)
            self.click(self.delete_data_source_button)
            self.confirm_deletion()
        except Exception as e:
            raise RuntimeError(f"Failed to delete data source: {str(e)}")

    def confirm_deletion(self):
        """Confirm the deletion of the data source."""
        self.click(self.confirm_delete_button)
        expect(self.page.locator(self.confirm_delete_toast)).to_have_text('Data source deleted')  # Optional: Wait for success message
