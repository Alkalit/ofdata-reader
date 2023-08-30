import httpx
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)


# todo init tqdm with from_byte in case file already partly downloaed
# TODO 'Content-Length': '16896477906' for progress bar
def download_file(filename: str, from_byte=0) -> str:
    if from_byte < 0:
        raise TypeError(f"Cannot download from {from_byte}'th byte.")

    headers = {
        'Range': 'bytes=%d-' % from_byte,
        'Accept-Encoding': 'gzip, deflate, br',
    }
    file_mode = "wb" if from_byte == 0 else "ab"

    logger.info("Initiated file downloading.")
    with httpx.stream(
        'GET',
        "https://ofdata.ru/open-data/download/egrul.json.zip",
        headers=headers,
    ) as response:
        file_size = int(response.headers['Content-Length'])

        with tqdm(
                initial=from_byte,
                total=file_size,
                unit_scale=True,
                unit_divisor=1024,
                unit="B",
                colour='#00ff00'
        ) as pgbar:
            with open(filename, file_mode) as file:
                num_bytes_downloaded = response.num_bytes_downloaded
                for chunk in response.iter_bytes():
                    file.write(chunk)
                    pgbar.update(response.num_bytes_downloaded - num_bytes_downloaded)
                    num_bytes_downloaded = response.num_bytes_downloaded
    return filename
