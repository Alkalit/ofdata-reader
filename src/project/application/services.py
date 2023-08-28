import json

from src.project.adapters.ofdata import download_file
from src.project.adapters.zipfile import yield_data, Filepath


def do_service(filepath: Filepath | None = None) -> None:
    if not filepath:
        downloaded_file_path = download_file()
    else:
        downloaded_file_path = filepath

        for json_data in yield_data(filepath=downloaded_file_path):
            json.loads(json_data)
