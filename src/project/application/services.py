import json
import orjson as json  # TODO for testing. Rollback later
from sqlite3 import Connection

from src.project.adapters.ofdata import download_file
from src.project.adapters.zipfile import yield_data, Filepath
from src.project.domain.models import Entry, Svokved, Svadresul, Adresrf, Svokvedosn, Gorod

KHABAROVSK_KRAI = "27"
OKVED_PREFIX = "62."
CITY_NAME = "ХАБАРОВСК"


def do_service(connection: Connection, filepath: Filepath | None = None) -> None:
    if not filepath:
        downloaded_file_path = download_file()
    else:
        downloaded_file_path = filepath

    for json_data in yield_data(filepath=downloaded_file_path, chunk=500):
        data: list[Entry] = json.loads(json_data)
        for entry in data:
            name: str = entry["name"]
            inn: str | None = entry["inn"]
            kpp: str | None = entry["kpp"]
            svadresul: Svadresul | None = entry["data"].get("СвАдресЮЛ")
            svokved: Svokved | None = entry["data"].get("СвОКВЭД")

            if svadresul is None:
                continue

            adresrf: Adresrf | None = svadresul.get("АдресРФ")
            if (adresrf is None) or (adresrf["КодРегион"] != KHABAROVSK_KRAI):  # TODO check with str.lower
                continue

            gorod: Gorod = adresrf.get("Город")
            if gorod is None:
                continue

            naimgorod: str | None = gorod.get("НаимГород")
            if (naimgorod is None) or (naimgorod != CITY_NAME):
                continue

            if not svokved:
                continue

            svokvedosn: Svokvedosn | None = svokved.get("СвОКВЭДОсн")
            if not svokvedosn:
                continue

            kodokved: str | None = svokvedosn.get("КодОКВЭД")
            if not kodokved.startswith(OKVED_PREFIX):
                continue

            dom, ulitza, kvartira, korpus = adresrf.get("Дом"), adresrf["Улица"]["НаимУлица"], adresrf.get(
                "Кварт"), adresrf.get("Корпус")

            cursor = connection.cursor()
            # No need for executemany since there is just a few entries that satisfy criteria
            # Care for the "replace" clause - it may lead to data losses; https://stackoverflow.com/a/4253806
            cursor.execute(
                """INSERT OR REPLACE INTO entity(name, inn, kpp, kodokved, ulitza, dom, korpus, kvartira) VALUES 
                    (? , ?, ?, ?, ?, ?, ?, ?)
                """,
                (name, inn, kpp, kodokved, ulitza, dom, korpus, kvartira)
            )
            connection.commit()
            # print(name, inn, kpp, kodokved, ulitza, korpus, dom, kvartira)
