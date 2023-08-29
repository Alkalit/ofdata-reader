from typing import TypedDict

Numeric = str
Date = str


class NaselPunkt(TypedDict):
    ТипНаселПункт: str
    НаимНаселПункт: str


class Region(TypedDict):
    ТипРегион: str
    НаимРегион: str


class Gorod(TypedDict):
    ТипГород: str
    НаимГород: str


class Ulitza(TypedDict):
    ТипУлица: str
    НаимУлица: str


class Rayon(TypedDict):
    ТипРайон: str
    НаимРайон: str


class Adresrf(TypedDict):
    Индекс: Numeric | None
    КодРегион: Numeric
    Регион: Region
    Дом: str | None
    Корпус: str | None
    Кварт: str | None
    Район: Rayon | None
    Город: Gorod | None
    НаселПункт: NaselPunkt | None
    Улица: Ulitza | None


class Svadresul(TypedDict):
    АдресРФ: Adresrf | None


class Svokvedosn(TypedDict):
    КодОКВЭД: str | None


class Svokved(TypedDict):
    СвОКВЭДОсн: Svokvedosn | None


class Data(TypedDict):
    ИНН: Numeric | None
    КПП: Numeric | None
    ОГРН: Numeric
    КодОПФ: Numeric
    СпрОПФ: str
    ДатаВып: Date
    СвОКВЭД: Svokved | None
    СвАдресЮЛ: Svadresul | None


class Entry(TypedDict):
    ogrn: Numeric
    inn: Numeric
    kpp: Numeric
    name: str
    full_name: str
    data: Data
