from io import BufferedReader
import zipfile
from typing import Generator, Any

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


def yield_data(filepath: Filepath, chunk: int | None = None) -> Generator[str, None, None]:
    """
    Yields a stream of individual files from archive in filepath
    """
    buffer_size = 10 * 1024 * 1024
    with open(filepath, 'rb') as file:
        with zipfile.ZipFile(BufferedReader(file, buffer_size=buffer_size)) as archive:
            if chunk is None:
                num_of_files = archive.namelist()
            else:
                num_of_files = archive.namelist()[:chunk]

            yield len(num_of_files)
            for sample in num_of_files:
                with archive.open(sample) as jsondata:
                    yield jsondata.read()
