import sqlite3
import logging
from sqlite3 import Connection

logger = logging.getLogger(__name__)


def get_connection(dbname: str) -> sqlite3.Connection:
    connection = sqlite3.connect(dbname)
    # Not much benefit atm, but may gain speed boost on high concurrent writes.
    connection.execute("PRAGMA journal_mode=WAL")
    logger.debug("Created a new connection to %s DB", dbname)
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


def save_entity(connection: Connection, *args):
    cursor = connection.cursor()
    # No need for executemany since there is just a few entries that satisfy criteria
    # Care for the "replace" clause - it may lead to data losses; https://stackoverflow.com/a/4253806
    cursor.execute(
        """INSERT OR REPLACE INTO entity(name, inn, kpp, kodokved, ulitza, dom, korpus, kvartira) VALUES 
            (? , ?, ?, ?, ?, ?, ?, ?)
        """,
        args
    )
    connection.commit()
    logger.debug("Saved %s into db", args)
