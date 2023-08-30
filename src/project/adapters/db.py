import sqlite3
import logging

logger = logging.getLogger(__name__)


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect("db.sqlite3")
    logger.debug("Created a new connection to db.sqlite3")
    return connection


def create_table(connection: sqlite3.Connection) -> None:
    cursor = connection.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS 
            entity(
            inn INTEGER NOT NULL PRIMARY KEY, 
            kpp INTEGER NOT NULL,
            name TEXT NOT NULL, 
            kodokved TEXT NOT NULL, 
            ulitza TEXT, 
            dom TEXT, 
            korpus TEXT, 
            kvartira TEXT)
            """
    )
    logger.debug("Initialized DB scheme.")
