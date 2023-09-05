import timeit
import logging
from pathlib import Path

from project.common.argparser import setup_argparser
from project.common.logging import setup_logging
from project.application.services import do_service
from project.adapters.db import get_connection, create_table


logger = logging.getLogger(__name__)


def main() -> None:
    setup_logging()
    parser = setup_argparser()
    args = parser.parse_args()

    db_root = Path("/db/")
    db_path = db_root / args.dbname
    connection = get_connection(dbname=db_path)
    # Not much benefit atm, but may gain speed boost on high concurrent writes.
    connection.execute("PRAGMA journal_mode=WAL")
    create_table(connection)
    logger.info("Successfully initialized application.")

    try:
        do_service(args.dbname, filepath=args.file, nfiles=args.nfiles)
        logger.info("Successfully completed dataset processing.")
    finally:
        connection.close()


if __name__ == '__main__':
    print(timeit.timeit(main, number=1))
