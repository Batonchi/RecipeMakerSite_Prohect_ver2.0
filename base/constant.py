import os

from dotenv import load_dotenv

load_dotenv()
# просто константы
DBNAME = os.environ.get('DBNAME')
HOST = os.environ.get('HOST')
PORT = os.environ.get('PORT')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
# нейросети
BOT_API_KEY = os.environ.get('BOT_API_KEY')
YANDEX_API_KEY = os.environ.get('YANDEX_API_KEY')
YANDEX_FOLDER_ID = os.environ.get('YANDEX_FOLDER_ID')
# почта уведомлений mail.ru
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
NOTIFICATION_MAIL_PASSWORD = os.environ.get('NOTIFICATION_MAIL_PASSWORD')
SUPPORT_MAIL_PASSWORD = os.environ.get('SUPPORT_MAIL_PASSWORD')

DATABASE_URL = f'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'