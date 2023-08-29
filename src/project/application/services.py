import json

from src.project.adapters.ofdata import download_file
from src.project.adapters.zipfile import yield_data, Filepath
from src.project.domain.models import Entry, Svokved, Svadresul, Adresrf, Svokvedosn


KHABAROVSK_KRAI = "27"


def do_service(filepath: Filepath | None = None) -> None:
    if not filepath:
        downloaded_file_path = download_file()
    else:
        downloaded_file_path = filepath

        for json_data in yield_data(filepath=downloaded_file_path, chunk=10):
            data: list[Entry] = json.loads(json_data)
            for entry in data:
                kodokved: str | None = None
                adresrf: Adresrf | None = None

                name: str = entry["name"]
                inn: str | None = entry["data"].get("ИНН")
                kpp: str | None = entry["data"].get("КПП")
                svokved: Svokved | None = entry["data"].get("СвОКВЭД")
                svadresul: Svadresul | None = entry["data"].get("СвАдресЮЛ")

                if not svadresul:
                    continue
                else:
                    adresrf: Adresrf | None = svadresul.get("АдресРФ")
                    if not adresrf or (adresrf["КодРегион"] != KHABAROVSK_KRAI):
                        continue

                if svokved:
                    svokvedosn: Svokvedosn | None = svokved.get("СвОКВЭДОсн")
                    if svokvedosn:
                        kodokved: str = svokvedosn.get("КодОКВЭД")

                print(name, inn, kpp, kodokved, adresrf)
