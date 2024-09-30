import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:3000/login")
USERNAME = os.getenv("USER_NAME", "qatest")
PASSWORD = os.getenv("PASSWORD", "test5")
TEST_DASHBOARD = 'screenshots/test_grafana_dashboard.png'
REFERENCE_DASHBOARD = 'screenshots/reference_screenshot.png'

# Database configuration for the MySQL data source
DATA_SOURCE_NAME = 'mysql'
MYSQL_HOST = 'host.docker.internal:3036'
MYSQL_DATABASE = 'my_dashboard'
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'root_password'

DEFAULT_QUERY = '''SELECT event_time, metric_value 
                    FROM timeseries_data 
                    WHERE category = 'Temperature' 
                    ORDER BY event_time;'''

DEFAULT_TIME_RANGE_FROM = '2024-09-01 00:00:00'
DEFAULT_TIME_RANGE_TO = '2024-09-03 23:59:59'

DEFAULT_DATA_SOURCE = 'mysql'
DEFAULT_VISUALIZATION = 'Time series'

# TODO: Divide this config into env_config, database_config, dashboard_config
