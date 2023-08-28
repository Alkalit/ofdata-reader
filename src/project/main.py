import requests
import argparse
import zipfile
import json
import timeit
from multiprocessing.pool import Pool, AsyncResult
from typing import Any, Generator

# resp = requests.get("https://ofdata.ru/open-data/download/egrul.json.zip")
serialized_json = Any


# Is used for performance testing to separated IO operations
# from CPU-bound
def get_data(chunk: int = 100) -> list[serialized_json]:
    result = []
    with zipfile.ZipFile('egrul.json.zip') as archive:
        for sample in archive.namelist()[:chunk]:
            with archive.open(sample) as jsondata:
                result.append(jsondata.read())
    return result


def yield_data(chunk: int = 100) -> Generator[str, None, None]:
    with zipfile.ZipFile('egrul.json.zip') as archive:
        for sample in archive.namelist()[:chunk]:
            with archive.open(sample) as jsondata:
                yield jsondata.read()


def do_service() -> None:
    with Pool(processes=4) as pool:
        fs: list[AsyncResult] = []
        for json_data in yield_data():
            future = pool.apply_async(json.loads, json_data)
            fs.append(future)

        for result in fs:
            result.wait()


def main() -> None:
    parser = argparse.ArgumentParser(
        "rostelekom downloader",
        description="Downloads sample dataset of russian legal entities from ofdata.ru"
    )
    parser.add_argument("--file", metavar="-f", nargs="?",
                        help="Process data from the specified file rather than downloading it")
    args = parser.parse_args()

    # do_service()


if __name__ == '__main__':
    print(timeit.timeit(main, number=1))
