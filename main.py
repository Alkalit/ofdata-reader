import requests
import zipfile
import json
import orjson
import timeit
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Executor, Future, wait, as_completed
from multiprocessing import Pool
from multiprocessing.pool import AsyncResult
# from line_profiler import profile
from typing import Any, Type, Generator
# from memory_profiler import profile
from abc import ABC

# samples = ['00001', '00002', '00003', '00004']
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


# @profile
def yield_data(chunk: int = 100) -> Generator[str, None, None]:
    with zipfile.ZipFile('egrul.json.zip') as archive:
        for sample in archive.namelist()[:chunk]:
            with archive.open(sample) as jsondata:
                yield jsondata.read()


def decoder(data: serialized_json, json_backend: BaseJsonBackend) -> None:
    de_jsoned = json_backend.loads(data)

# @profile
def main() -> None:
    with Pool(processes=4) as pool:
        fs: list[AsyncResult] = []
        # json_backend = BuiltinJsonBackend()
        # json_backend = OrjsonBackend()
        with zipfile.ZipFile('egrul.json.zip') as archive:
            for sample in archive.namelist()[:1000]:
                with archive.open(sample) as json_data:
                    data = json_data.read()
                    # print(f'Enqueuing file {sample}, size {len(data) / 1024 / 1024} Mb')
                    # future = pool.apply_async(json.loads, data)
                    future = pool.apply_async(orjson.loads, data)
                    fs.append(future)

        for result in fs:
            result.wait()

def main_futures() -> None:
    with ProcessPoolExecutor(max_workers=4) as pool:
        fs: list[Future] = []
        # json_backend = BuiltinJsonBackend()
        json_backend = OrjsonBackend()
        with zipfile.ZipFile('egrul.json.zip') as archive:
            for sample in archive.namelist()[:1000]:
                with archive.open(sample) as json_data:
                    # print(f'Enqueuing file {sample}, size {len(data) / 1024 / 1024} Mb')
                    # future = pool.submit(decoder, json_data.read(), json_backend)
                    # future = pool.submit(json.loads, json_data.read())
                    future = pool.submit(orjson.loads, json_data.read())
                    fs.append(future)

        wait(fs)


SUPPORTED_BACKENDS = {
    'builtin': BuiltinJsonBackend,
    'orjson': OrjsonBackend,
}

if __name__ == '__main__':
    print(timeit.timeit(main, number=1))
    # print(timeit.timeit(main_futures, number=1))
