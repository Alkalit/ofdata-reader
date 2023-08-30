import timeit

from project.common.argparser import configure_argparser
from project.common.logging import setup_logging
from project.application.services import do_service
from project.adapters.db import get_connection, create_table


def main() -> None:
    setup_logging()
    parser = configure_argparser()
    args = parser.parse_args()

    connection = get_connection()
    create_table(connection)

    do_service(connection, filepath=args.file)

    connection.close()


if __name__ == '__main__':
    print(timeit.timeit(main, number=1))
