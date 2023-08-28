import argparse
import timeit

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

    do_service(filepath=args.file)


if __name__ == '__main__':
    print(timeit.timeit(main, number=1))
