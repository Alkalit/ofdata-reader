import requests

# resp = requests.head("https://ofdata.ru/open-data/download/egrul.json.zip")
# print(resp.headers)


import zipfile
import json
import orjson
import timeit
# from line_profiler import profile
from typing import Any, Type, Generator
from memory_profiler import profile
from abc import ABC

samples = ['00001', '00002', '00003', '00004']
deserialized_json = Any


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
        return json.loads(data, **options)

    def dumps(self, obj: Any, **options) -> str:
        return self._lib.dumps(
            obj,
            option=orjson.OPT_INDENT_2,
            **options,
        ).decode('utf-8')

def get_data(chunk: int = 100) -> list[deserialized_json]:
    result = []
    with zipfile.ZipFile('egrul.json.zip') as archive:
        for sample in archive.namelist()[:chunk]:
            with archive.open(sample) as jsondata:
                result.append(jsondata.read())
    return result

def yield_data(chunk: int = 100) -> Generator[deserialized_json, None, None]:
    with zipfile.ZipFile('egrul.json.zip') as archive:
        for sample in archive.namelist()[:chunk]:
            with archive.open(sample) as jsondata:
                yield jsondata.read()

def decoder(data: deserialized_json, json_backend: BaseJsonBackend) -> None:
    de_jsoned = json_backend.loads(data)

def main() -> None:
    # json_backend = BuiltinJsonBackend() # 1000 files - 136 secs
    json_backend = OrjsonBackend() # 1000 files - 130 secs
    for data in get_data():
        decoder(data, json_backend)


SUPPORTED_BACKENDS = {
    'builtin': BuiltinJsonBackend,
    'orjson': OrjsonBackend,
}

if __name__ == '__main__':
    # func(json_backend)
    print(timeit.timeit(main, number=1))