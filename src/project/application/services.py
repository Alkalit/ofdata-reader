import os
import orjson as json
import logging
from tqdm import tqdm
from multiprocessing.pool import Pool, AsyncResult
from contextlib import closing

from project.adapters.db import save_entity, get_connection
from project.adapters.ofdata import OfdataGateway
from project.adapters.zipfile import yield_data, Filepath
from project.domain.models import Entry, Svokved, Svadresul, Adresrf, Svokvedosn, Gorod

logger = logging.getLogger(__name__)

KHABAROVSK_KRAI = "27"
OKVED_PREFIX = "62."
CITY_NAME = "ХАБАРОВСК"
DEFAULT_FILE_NAME = 'egrul.json.zip'


# Note: this typehint looks ugly, but it's either Any or refactor to use proper (data)classes to border out
# domain entities
def filter_out(entry: Entry) -> \
        tuple[
            str, str, str, str | None, str, str | None, str | None, str | None] | None:  # You're one ugly motherfucker
    name = entry["name"]
    inn = entry["inn"]
    kpp = entry["kpp"]
    svadresul: Svadresul | None = entry["data"].get("СвАдресЮЛ")
    svokved: Svokved | None = entry["data"].get("СвОКВЭД")

    if svadresul is None:
        return

    adresrf: Adresrf | None = svadresul.get("АдресРФ")
    if (adresrf is None) or (adresrf["КодРегион"] != KHABAROVSK_KRAI):  # TODO check with str.lower
        return

    gorod: Gorod = adresrf.get("Город")
    if gorod is None:
        return

    naimgorod: str | None = gorod.get("НаимГород")
    if (naimgorod is None) or (naimgorod != CITY_NAME):
        return

    if not svokved:
        return

    svokvedosn: Svokvedosn | None = svokved.get("СвОКВЭДОсн")
    if not svokvedosn:
        return

    kodokved: str | None = svokvedosn.get("КодОКВЭД")
    if not kodokved.startswith(OKVED_PREFIX):
        return

    dom, ulitza, kvartira, korpus = adresrf.get("Дом"), adresrf["Улица"]["НаимУлица"], adresrf.get(
        "Кварт"), adresrf.get("Корпус")

    return name, inn, kpp, kodokved, ulitza, dom, korpus, kvartira


def process_entity_json(json_data: str, dbname: str):
    data: list[Entry] = json.loads(json_data)
    for entry in data:
        result = filter_out(entry)

        if result is None:
            continue

        with closing(get_connection(dbname)) as connection:
            save_entity(connection, *result)


def do_service(
        dbname: str,
        filepath: Filepath | None = None,
        nfiles: int | None = None,
) -> None:

    if not filepath:
        filename = DEFAULT_FILE_NAME
        ofdata_client = OfdataGateway()
        if not os.path.isfile(filename):
            from_byte = 0
            logger.info("No dataset file found. Downloading from the start")
        else:
            from_byte = os.path.getsize(filename)
            logger.info("A dataset file is found. Downloading from %s byte", from_byte)

        downloaded_file_path = ofdata_client.download_file(filename, from_byte=from_byte)
    else:
        downloaded_file_path = filepath
        logger.info("Dataset file is specified. Skipping downloading")

    logger.debug("Got file: %s", downloaded_file_path)
    generator = yield_data(filepath=downloaded_file_path, chunk=nfiles)
    fs: list[AsyncResult] = []

    num_of_files = next(generator)
    with tqdm(total=num_of_files, desc="Processing the archive.") as pgbar:
        # 2-4 workers is sufficient. I hesitate to propagate it to the program's arguments.
        with Pool(processes=4) as pool:
            for json_data in generator:
                pool.apply_async(process_entity_json, (json_data, dbname))
                pgbar.update()

            # Note: we could possibly add here another one progressbar
            # But that's redundant atm. IO is the main bottleneck.
            for future in fs:
                future.wait()
