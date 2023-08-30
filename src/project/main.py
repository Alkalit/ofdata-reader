import timeit
import sqlite3

from project.common.argparser import configure_argparser
from project.common.logging import setup_logging
from src.project.application.services import do_service


def main() -> None:
    setup_logging()
    parser = configure_argparser()
    args = parser.parse_args()
    connection = sqlite3.connect("db.sqlite3")
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

    do_service(connection, filepath=args.file)

    connection.close()


if __name__ == '__main__':
    print(timeit.timeit(main, number=1))
