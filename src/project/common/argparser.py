import argparse


def setup_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        "rostelekom downloader",
        description="Downloads sample dataset of russian legal entities from ofdata.ru"
    )
    parser.add_argument("--file", metavar="-f", nargs="?",
                        help="Process data from the specified file rather than downloading it")

    return parser