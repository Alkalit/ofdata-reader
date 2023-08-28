import requests
import zipfile
import json
import orjson
import timeit
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Future, wait
from typing import Any, Generator
from abc import ABC

# resp = requests.get("https://ofdata.ru/open-data/download/egrul.json.zip")
serialized_json = Any


class BaseJsonBackend(ABC):

    def loads(self, data: bytes | bytearray | str | memoryview, **options) -> Any:
        ...

    def dumps(self, obj: Any, **options) -> str:
        """
        obj - A python object to be serialized.
        options - options for the specific backend
        """
        ...


class BuiltinJsonBackend(BaseJsonBackend):

    def __init__(self):
        self._lib = json

    def loads(self, data: bytes | bytearray | str | memoryview, **options) -> Any:
        return self._lib.loads(data, **options)

    def dumps(self, obj: Any, **options) -> str:
        return self._lib.dumps(obj, **options)


class OrjsonBackend(BaseJsonBackend):

    def __init__(self):
        self._lib = orjson

    def loads(self, data: bytes | bytearray | str | memoryview, **options) -> Any:
        return self._lib.loads(data)

    def dumps(self, obj: Any, **options) -> str:
        return self._lib.dumps(
            obj,
            option=orjson.OPT_INDENT_2,
            **options,
        ).decode('utf-8')


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


def main() -> None:
    with ProcessPoolExecutor(max_workers=4) as pool:
        fs: list[Future] = []
        with zipfile.ZipFile('egrul.json.zip') as archive:
            for sample in archive.namelist()[:1000]:
                with archive.open(sample) as json_data:
                    future = pool.submit(json.loads, json_data.read())
                    fs.append(future)

        wait(fs)


if __name__ == '__main__':
    print(timeit.timeit(main, number=1))
