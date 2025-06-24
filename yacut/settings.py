import os

from dotenv import load_dotenv

SHORT_URL_ID_LENGTH = 6
MAX_RETRY_FOR_SHORT_ID_GENERATION = 10

URL_MAX_LENGTH = 2048
SHORT_ID_MAX_LENGTH = 16

SHORT_ID_PATTERN = rf'^[A-Za-z0-9]{{1,{SHORT_ID_MAX_LENGTH}}}$'

# yandex disk
API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
load_dotenv()
DISK_TOKEN = os.environ.get('DISK_TOKEN')
APP_NAME = os.environ.get('APP_NAME')
AUTH_HEADERS = {
    'Authorization': f'OAuth {DISK_TOKEN}'
}
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    DISK_TOKEN = os.getenv('DISK_TOKEN')
