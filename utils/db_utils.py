import logging
import mariadb
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        logger.info("Database connection established successfully.")
        return connection

    except mariadb.Error as e:
        logger.error(f"Error establishing database connection: {e}")
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
            logger.info("Database connection closed successfully.")
        except mariadb.Error as e:
            logger.error(f"Error closing database connection: {e}")
