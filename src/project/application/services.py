import json
import zipfile
from multiprocessing.pool import Pool, AsyncResult
from typing import Any, Generator
import requests

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
    filename = 'egrul.json.zip'
    response = requests.get("https://ofdata.ru/open-data/download/egrul.json.zip", stream=True)
    chunk_size = 1024 * 1024  # 1 mb
    with open(filename) as file:
        for chunk in response.iter_content(chunk_size=chunk_size):
            file.write(chunk)
    return filename


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
