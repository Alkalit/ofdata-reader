import requests


def download_file() -> str:
    filename = 'egrul.json.zip'  # TODO hardcoded filename
    # TODO hardcoded url
    response = requests.get("https://ofdata.ru/open-data/download/egrul.json.zip", stream=True)
    chunk_size = 1024 * 1024  # 1 mb
    with open(filename) as file:
        for chunk in response.iter_content(chunk_size=chunk_size):
            file.write(chunk)
    return filename