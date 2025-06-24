# async-yacut

### Описание
Приложение YaCut - учебный проект в рамках курса "Python-разработчик" от Яндекс.Практикум.
Предоставляет возможности:
- укорачивать ссылки;
- загружать файлы на Яндекс Диск и скачивать их по коротким ссылкам.
Доступен API, который позволяет:
- укорачивать ссылки;
- получать оригинальную ссылку по короткой.

### Технологии:

- Python 3.12.1
- Flask, Flask-SQLAlchemy, Flask-WTF


### Автор: [Вадим Белясов](https://github.com/hkkmrmnq), [проект](https://github.com/hkkmrmnq/async-yacut)


### Как запустить проект Yacut:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:hkkmrmnq/async-yacut.git
```

```
cd yacut
```

Cоздать виртуальное окружение:

```shell
py -3.12 -m venv venv
```

Активировать виртуальное окружение:

```shell
venv/scripts/activate
```

Установить зависимости из файла requirements.txt:

```shell
py -m pip install --upgrade pip
```

```shell
py -m pip install -r requirements.txt
```

Создать в директории проекта файл .env с переменными окружения:

```
FLASK_APP=yacut
FLASK_DEBUG=1
DATABASE_URI='sqlite:///db.sqlite3'
SECRET_KEY='your_secrect_key'
DISK_TOKEN='your_yandex_disk_token'
APP_NAME='your_yandex_disk_app_name'
```

Создать базу данных и применить миграции:

```
flask db upgrade
```

Запустить проект:

```
flask run
```
