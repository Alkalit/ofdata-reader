import requests

# resp = requests.head("https://ofdata.ru/open-data/download/egrul.json.zip")
# print(resp.headers)


import zipfile
import json
import orjson
import timeit
# from line_profiler import profile
from typing import Any, Type
from memory_profiler import profile
from abc import ABC

samples = ['00001', '00002', '00003', '00004']


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

# @profile
def func(json_backend: BaseJsonBackend):
    with zipfile.ZipFile('egrul.json.zip') as archive:
        # for sample in samples:
        for sample in archive.namelist()[:100]:
            with archive.open(sample) as jsondata:
            # with open(f'{sample}.indent.json', 'w', encoding='utf8') as tmp:
                de_jsoned = json_backend.loads(jsondata.read())
                # tmp.write(
                #     json_backend.dumps(de_jsoned)
                # )

SUPPORTED_BACKENDS = {
    'builtin': BuiltinJsonBackend,
    'orjson': OrjsonBackend,
}

if __name__ == '__main__':
    json_backend = BuiltinJsonBackend() # 1000 files - 136 secs
    # json_backend = OrjsonBackend() # 1000 files - 130 secs
    # func(json_backend)
    print(timeit.timeit(lambda: func(json_backend), number=1))
    # func()