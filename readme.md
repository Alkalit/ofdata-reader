# Описание
Тестовое задание: Разработайте программу на Python, которая выполняет следующие действия:
Читает файл Единого государственного реестр юридических лиц (https://ofdata.ru/open-data/download/egrul.json.zip), выбирает компании, занимающиеся разработкой программного обеспечения (Группировка ОКВЭД 62), зарегистрированные в г. Хабаровск и записывает информацию о выбранных компаниях (название компании, код ОКВЭД, ИНН, КПП и место регистрации ЮЛ) в базу данных.

Результат требуется представить в виде ссылки на репозиторий GitHub

# Установка и запуск
`git clone  https://github.com/Alkalit/ofdata-reader.git`

В директории проекта:

Установк: `pip install -e .` (требуется pip >= 23)

Запуск: `python src/project/main.py`

Помощь: `python src/project/main.py -h`

Проект тестировался на python 3.10 и 3.11

# Особенности:
- Продолжение загрузски архива при обрыве соединения или преждевременном завершении программы.
- Параллелизм: скачанные файлы обрабатываются конкурентно пучком процессов.
