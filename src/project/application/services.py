import json
import zipfile
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