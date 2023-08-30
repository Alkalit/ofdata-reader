import zipfile
from typing import Generator, Any

# Is used for performance testing to separated IO operations
# from CPU-bound
serialized_json = Any
Filepath = str


def get_data(chunk: int = 100) -> list[serialized_json]:
    result = []
    with zipfile.ZipFile('egrul.json.zip') as archive:
        for sample in archive.namelist()[:chunk]:
            with archive.open(sample) as jsondata:
                result.append(jsondata.read())
    return result


# TODO by default should iterate over all files.
def yield_data(filepath: Filepath, chunk: int = 100) -> Generator[str, None, None]:
    """
    Yields a stream of individual files from archive in filepath
    """
    with zipfile.ZipFile(filepath) as archive:
        for sample in archive.namelist()[:chunk]:
            with archive.open(sample) as jsondata:
                yield jsondata.read()
