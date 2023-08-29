import json

from src.project.adapters.ofdata import download_file
from src.project.adapters.zipfile import yield_data, Filepath


def do_service(filepath: Filepath | None = None) -> None:
    if not filepath:
        downloaded_file_path = download_file()
    else:
        downloaded_file_path = filepath

        for idx, json_data in enumerate(yield_data(filepath=downloaded_file_path, chunk=100)):
            data = json.loads(json_data)
            for entry in data:
                kodokved: str | None = None
                adresrf: dict | None = None
                name: str = entry["name"]
                inn: str | None = entry["data"].get("ИНН")
                kpp: str | None = entry["data"].get("КПП")
                svokded: dict | None = entry["data"].get("СвОКВЭД")
                svadresul: dict | None = entry["data"].get("СвАдресЮЛ")

                if not svadresul:
                    continue
                else:
                    adresrf = svadresul.get("АдресРФ")
                    if not adresrf or (adresrf["КодРегион"] != "27"):
                        continue

                if svokded:
                    svokvedosn: str | dict = svokded.get("СвОКВЭДОсн")
                    if svokvedosn:
                        kodokved = svokvedosn.get("КодОКВЭД")

                print(name, inn, kpp, kodokved, adresrf)
