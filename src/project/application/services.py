import json
from multiprocessing.pool import Pool, AsyncResult

from src.project.adapters.ofdata import download_file
from src.project.adapters.zipfile import yield_data, Filepath


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
