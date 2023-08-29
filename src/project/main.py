import argparse
import timeit
import sqlite3

from src.project.application.services import do_service


def configure_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        "rostelekom downloader",
        description="Downloads sample dataset of russian legal entities from ofdata.ru"
    )
    parser.add_argument("--file", metavar="-f", nargs="?",
                        help="Process data from the specified file rather than downloading it")

    return parser


def main() -> None:
    parser = configure_argparser()
    args = parser.parse_args()
    connection = sqlite3.connect("db.sqlite3")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS entity(name, inn, kpp, kodokved, ulitza, dom, korpus, kvartira)")

    do_service(connection, filepath=args.file)

    connection.close()


if __name__ == '__main__':
    print(timeit.timeit(main, number=1))
