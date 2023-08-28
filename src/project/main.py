import requests
import argparse
import zipfile
import json
import timeit
from multiprocessing.pool import Pool, AsyncResult
from typing import Any, Generator

serialized_json = Any
Filepath = str


# Is used for performance testing to separated IO operations
# from CPU-bound
def get_data(chunk: int = 100) -> list[serialized_json]:
    result = []
    with zipfile.ZipFile('egrul.json.zip') as archive:
        for sample in archive.namelist()[:chunk]:
            with archive.open(sample) as jsondata:
                result.append(jsondata.read())
    return result


def yield_data(filepath: Filepath, chunk: int = 100) -> Generator[str, None, None]:
    with zipfile.ZipFile(filepath) as archive:
        for sample in archive.namelist()[:chunk]:
            with archive.open(sample) as jsondata:
                yield jsondata.read()


def download_file() -> str:
    # resp = requests.get("https://ofdata.ru/open-data/download/egrul.json.zip")
    return '/root'


def do_service(filepath: Filepath | None = None) -> None:
    if not filepath:
        downloaded_file_path = download_file()
    else:
        downloaded_file_path = filepath

    with Pool(processes=4) as pool:
        fs: list[AsyncResult] = []
        for json_data in yield_data(filepath=downloaded_file_path):
            future = pool.apply_async(json.loads, json_data)
            fs.append(future)

        for result in fs:
            result.wait()


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
