from playwright.sync_api import expect

from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.menu_button = '#mega-menu-toggle'
        self.connections_menu = 'button[aria-label*="section Connections"]'
        self.data_sources_menu = '//span[text()="Data sources"]'
        self.data_source_title = '.css-swtwop'

    def open_data_source(self):
        """Open the data sources menu from the home page."""
        try:
            self.click(self.menu_button)
            self.page.wait_for_selector(self.connections_menu)  # Wait for the Connections menu to be visible

            # Check if the Connections menu is expanded or collapsed
            if 'Collapse' not in self.get_attribute(self.connections_menu):
                self.click(self.connections_menu)
                # Optional: Wait for connections menu to expand fully
                self.page.wait_for_timeout(500)  # Give some time for the menu to expand

            self.click(self.data_sources_menu)
            # Wait for the data source title to be visible to confirm navigation
            expect(self.page.locator(self.data_source_title)).to_be_visible(timeout=5000)

        except Exception as e:
            raise RuntimeError(f"Failed to open data sources: {str(e)}")

