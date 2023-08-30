import requests


# TODO 'Content-Length': '16896477906' for progress bar
def download_file(filename: str, from_byte=0) -> str:
    if from_byte < 0:
        raise TypeError(f"Cannot download from {from_byte}'th byte.")

    chunk_size = 1024 * 1024  # 1 mb
    headers = {'Range': 'bytes=%d-' % from_byte}
    file_mode = "wb" if from_byte == 0 else "ab"

    response = requests.get(
        "https://ofdata.ru/open-data/download/egrul.json.zip",
        stream=True,
        headers=headers,
    )

    with open(filename, file_mode) as file:
        for chunk in response.iter_content(chunk_size=chunk_size):
            file.write(chunk)
    return filename
