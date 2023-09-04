import httpx
import logging
from io import TextIOWrapper
from typing import Generator
from tenacity import retry, retry_if_exception_type
from tqdm import tqdm

logger = logging.getLogger(__name__)

__all__ = ['OfdataGateway']


class OfdataGateway:
    def __init__(self, session: httpx.Client = None):
        self._session = session or httpx.Client()

    def download_file(self, filename: str, from_byte=0) -> str:
        if from_byte < 0:
            raise TypeError(f"Cannot download from {from_byte} byte.")

        self._from_byte = from_byte

        url = "https://ofdata.ru/open-data/download/egrul.json.zip"
        file_size = self._get_file_size(url)

        file_mode = "wb" if from_byte == 0 else "ab"

        logger.info("Initiated file downloading.")
        with tqdm(
                desc="Downloading the archive",
                initial=from_byte,
                total=file_size,
                unit_scale=True,
                unit_divisor=1024,
                unit="B",
        ) as pgbar:
            self.pgbar = pgbar
            with open(filename, file_mode) as file:
                self._download_file(url, file)
        return filename

    def _get_file_size(self, url: str) -> int:
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
        }
        resp = self._session.head(url, headers=headers)
        content_length = resp.headers['Content-Length']
        return int(content_length)

    @retry(retry=retry_if_exception_type(httpx.RemoteProtocolError))
    def _download_file(self, url: str, file: TextIOWrapper):
        headers = {
            'Range': 'bytes=%d-' % self._from_byte,
            'Accept-Encoding': 'gzip, deflate, br',
        }
        with self._session.stream(
                'GET',
                url,
                headers=headers,
        ) as response:
            num_bytes_downloaded: int = response.num_bytes_downloaded
            for chunk in response.iter_bytes():
                file.write(chunk)
                self._from_byte += len(chunk)
                self.pgbar.update(response.num_bytes_downloaded - num_bytes_downloaded)
                num_bytes_downloaded = response.num_bytes_downloaded
