import logging
import time

from pages.base_page import BasePage
from utils.config import DEFAULT_DASHBOARD_QUERY, DEFAULT_TIME_RANGE_FROM, DEFAULT_TIME_RANGE_TO


class DashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.build_dashboard_link = '[aria-label="Create a dashboard"]'
        self.dashboard_container = '//h1[contains(text(),"Start your new dashboard")]'
        self.add_visualization_button = 'button[data-testid*="Create new panel"]'
        self.select_data_source_dialog = '.css-1fuqvhh'
        self.mysql_button = '//span[contains(text(),"mysql")]'

        self.edit_dashboard_panel = '[data-testid*="Panel editor content"]'
        self.data_source_dropdown = '#data-source-picker'
        self.select_data_source_dialog = '.css-1fuqvhh'
        self.change_visualization_button = 'button[aria-label="Change Visualization"]'
        self.search_visualization_input = 'input[placeholder*="Search for"]'
        self.time_series_visualization_button = '[aria-label*="Time series"]'

        self.search_options_input = '[placeholder="Search options"]'
        self.panel_options_toggle = '[data-testid*="Panel options toggle"]'
        self.panel_title_input = '#PanelFrameTitle'
        self.panel_description_input = '#description-text-area'

        self.tooltip_toggle = '#button-Tooltip'
        self.tooltip_single_mode_radio = '[id="option-single-tooltip.mode"]'

        self.graph_styles_toggle = '#button-Tooltip'
        self.graph_lines_radio = '[id="option-line-custom.drawStyle"]'
        self.graph_linear_radio = '[id="option-linear-custom.lineInterpolation"]'

        self.select_time_range_button = '.css-1ueg5w'
        self.time_range_from_input = '[data-testid*="Time Range from"]'
        self.time_range_to_input = '[data-testid*="Time Range to"]'
        self.apply_time_range_button = '[data-testid*="TimePicker submit"]'

        self.dataset_input = '//label[contains(text(),"Dataset")]/following-sibling::div'
        self.code_radio = '[id*="option-code-radio"]'
        self.query_input = '[class="monaco-scrollable-element editor-scrollable vs-dark"]'
        self.run_query_button = '//button/span[contains(text(),"Run query")]'

        self.save_dashboard_button = '[title="Apply changes and save dashboard"]'
        self.apply_dashboard_button = '[title="Apply changes and go back to dashboard"]'

        self.dashboard_panel = '.u-over'
        self.panel_title = '[class*="panel-title"]'
        self.legend_title = '[class*="legend-title"]'

    # def add_query(self):
    #     # TODO: remove query to test data
    #     query = "SELECT event_time, metric_value FROM timeseries_data WHERE category = 'Temperature' ORDER BY event_time;"
    #     self.page.wait_for_selector(self.edit_dashboard_panel)
    #     self.click(self.code_radio)
    #     self.click(self.query_input)
    #     self.page.keyboard.insert_text(query)
    #     self.click(self.run_query_button)

    def add_query(self, query=DEFAULT_DASHBOARD_QUERY):
        """
        Adds the SQL query to the dashboard's query input.

        :param query: SQL query string to add to the query input
        """
        try:
            self.page.wait_for_selector(self.edit_dashboard_panel)
            self.click(self.code_radio)
            self.click(self.query_input)
            self.page.keyboard.insert_text(query)
            self.click(self.run_query_button)
            logging.info("Query successfully added and executed.")
        except Exception as e:
            logging.error(f"Failed to add or execute query: {str(e)}")
            raise

    def update_time_range(self, time_from=DEFAULT_TIME_RANGE_FROM, time_to=DEFAULT_TIME_RANGE_TO):
        """
        Updates the time range for the dashboard panel.

        :param time_from: Start time range
        :param time_to: End time range
        """
        try:
            self.click(self.select_time_range_button)
            self.fill(self.time_range_from_input, time_from)
            self.fill(self.time_range_to_input, time_to)
            self.click(self.apply_time_range_button)
            logging.info(f"Time range successfully updated from {time_from} to {time_to}.")
        except Exception as e:
            logging.error(f"Failed to update time range: {str(e)}")
            raise

    def configure_tooltip(self):
        """
        Configures the tooltip settings for the dashboard visualization.
        """
        try:
            self.click(self.tooltip_toggle)
            self.click(self.tooltip_single_mode_radio)
            logging.info("Tooltip successfully configured.")
        except Exception as e:
            logging.error(f"Failed to configure tooltip: {str(e)}")
            raise

    def configure_graph_styles(self):
        """
        Configures the graph styles such as line and interpolation modes.
        """
        try:
            self.click(self.graph_styles_toggle)
            self.click(self.graph_lines_radio)
            self.click(self.graph_linear_radio)
            logging.info("Graph styles successfully configured.")
        except Exception as e:
            logging.error(f"Failed to configure graph styles: {str(e)}")
            raise

    def add_time_series_visualization(self, title='Weather data', description='Weather data from 1st to 3rd September'):
        """
        Adds a time series visualization to the dashboard.

        :param title: Title for the visualization panel
        :param description: Description for the visualization panel
        """
        try:
            self.click(self.change_visualization_button)
            self.click(self.time_series_visualization_button)
            self.fill(self.panel_title_input, title)
            self.fill(self.panel_description_input, description)
            self.configure_tooltip()
            self.configure_graph_styles()
            logging.info("Time series visualization successfully added.")
        except Exception as e:
            logging.error(f"Failed to add time series visualization: {str(e)}")
            raise

    def add_visualization(self, data_source='mysql', visualization_type='Time series'):
        self.add_query()
        self.update_time_range()
        self.add_time_series_visualization()

    def add_dashboard(self):
        """
        Navigates to the dashboard creation page and starts the process.
        """
        try:
            self.click(self.build_dashboard_link)
            self.page.wait_for_selector(self.dashboard_container)
            self.click(self.add_visualization_button)
            self.page.wait_for_selector(self.mysql_button)
            self.click(self.mysql_button)
            logging.info("Dashboard creation started.")
        except Exception as e:
            logging.error(f"Failed to create dashboard: {str(e)}")
            raise

    def save_and_apply(self):
        """
        Saves and applies the dashboard changes.
        """
        try:
            self.click(self.apply_dashboard_button)
            logging.info("Dashboard changes successfully applied.")
        except Exception as e:
            logging.error(f"Failed to apply dashboard changes: {str(e)}")
            raise

    def build_dashboard(self):
        """
        Full process to build a dashboard by adding a data source, time series visualization,
        and applying all changes.
        """
        try:
            self.add_dashboard()
            self.add_visualization()
            self.save_and_apply()
            logging.info("Dashboard successfully built.")
        except Exception as e:
            logging.error(f"Failed to build dashboard: {str(e)}")
            raise



