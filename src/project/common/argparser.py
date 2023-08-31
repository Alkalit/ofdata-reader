import argparse
import logging

logger = logging.getLogger(__name__)


def setup_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        "Ofdata test dataset downloader",
        description="Downloads a sample dataset of russian legal entities from ofdata.ru"
    )
    parser.add_argument("--file", "-f", nargs="?",
                        help="Process the data from the specified file rather than downloading it.")
    parser.add_argument("--nfiles", "-n", nargs="?", type=int,
                        help="Process first n files in the archive.")
    parser.add_argument("--dbname", "-d", nargs="?", default="db.sqlite3",
                        help="Database name where to save the result.")

    logger.debug("Argparser is successfully configured.")
    return parser
