import csv
import os

import mariadb
import pytest
from utils.db_utils import create_db_connection, close_db_connection


@pytest.fixture
def create_database_connection() -> mariadb.Connection:
    """
    Fixture to create a database connection for tests.
    Yields a connection object for the duration of the test.
    """
    conn = create_db_connection()
    yield conn
    close_db_connection(conn)  # Cleanup: Close the database connection after the test is done


@pytest.fixture
def create_table_timeseries(create_database_connection):
    """
    Fixture to create a timeseries_data table for tests.
    Cleans up existing data before each test.
    """
    conn = create_database_connection
    with conn.cursor() as cur:
        cur.execute(''' 
            CREATE TABLE IF NOT EXISTS timeseries_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_time DATETIME NOT NULL,
                metric_value FLOAT NOT NULL,
                category VARCHAR(50),
                description TEXT
            );
        ''')
        # Clean up existing data
        cur.execute('DELETE FROM timeseries_data;')
    yield conn


def insert_data_from_csv(cur, csv_file_path: str) -> int:
    """
    Inserts data from a CSV file into the database.

    Args:
        cur (mariadb.Cursor): The cursor object to execute queries.
        csv_file_path (str): The path to the CSV file.

    Returns:
        int: The number of rows inserted.
    """
    csv_row_count = 0  # Counter for number of rows in the file

    try:
        with open(csv_file_path, mode='r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row

            for row in reader:
                cur.execute(
                    "INSERT INTO timeseries_data (event_time, metric_value, category, description) VALUES (?, ?, ?, ?)",
                    row
                )
                csv_row_count += 1
    except FileNotFoundError:
        pytest.fail(f"CSV file not found: {csv_file_path}")
    except Exception as e:
        pytest.fail(f"Error reading CSV file {csv_file_path}: {e}")

    return csv_row_count


def test_load_data(create_table_timeseries):
    """
    Test loading data from a CSV file into the timeseries_data table.
    Validates that the number of records matches the number of rows in the CSV file.
    """
    conn = create_table_timeseries
    current_dir = os.path.dirname(__file__)
    csv_file_path = os.path.join(current_dir, 'test_data', 'weather_data.csv')

    # Error handling for file existence
    if not os.path.isfile(csv_file_path):
        pytest.fail(f"CSV file not found: {csv_file_path}")

    try:
        with conn.cursor() as cur:
            # Insert data and get row count from CSV
            csv_row_count = insert_data_from_csv(cur, csv_file_path)

            # Commit changes
            conn.commit()

            # Get number of records from the DB
            cur.execute("SELECT COUNT(*) FROM timeseries_data")
            db_row_count = cur.fetchone()[0]  # Fetch the first element, which is the row count

        # Assert records are the same as present in the file
        assert csv_row_count == db_row_count, (
            f"Row count mismatch: CSV has {csv_row_count} rows, but DB has {db_row_count} records."
        )

    except Exception as e:
        pytest.fail(f"Database operation failed: {e}")
