import csv
import logging
import mariadb
from typing import Optional

import pytest

from utils.config import CREATE_QUERY


def create_db_connection() -> Optional[mariadb.Connection]:
    """
    Create a database connection to the MariaDB database.

    Returns:
        Optional[mariadb.Connection]: A connection object if successful, None otherwise.
    """
    connection = None
    try:
        # Establish the connection
        connection = mariadb.connect(
            host="127.0.0.1",
            port=3036,
            user="root",
            password="root_password",
            database="my_dashboard",
        )
        logging.info("Database connection established successfully.")
        return connection

    except mariadb.Error as e:
        logging.error(f"Error establishing database connection: {e}")
        raise


def close_db_connection(connection: mariadb.Connection) -> None:
    """
    Close the database connection.

    Args:
        connection (mariadb.Connection): The connection object to close.
    """
    if connection:
        try:
            connection.close()
            logging.info("Database connection closed successfully.")
        except mariadb.Error as e:
            logging.error(f"Error closing database connection: {e}")


def create_table_in_database(cur, query: str = CREATE_QUERY):
    """Creates table in the database as per query"""

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


def fetch_rows_count(cur, table='timeseries_data'):
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    db_row_count = cur.fetchone()[0]
    return db_row_count
