import sqlite3


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect("../../../db.sqlite3")


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
