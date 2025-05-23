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
# нейросети yandex
YANDEX_API_KEY = os.environ.get('YANDEX_API_KEY')
YANDEX_FOLDER_ID = os.environ.get('YANDEX_FOLDER_ID')
# нейросеть giga
SBER_CLIENT_ID = os.environ.get('SBER_CLIENT_ID')
SCOPE = os.environ.get('SCOPE')
AUTHORIZATION_KEY = os.environ.get('AUTH_SBER_KEY')
# почта уведомлений mail.ru
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
NOTIFICATION_MAIL_PASSWORD = os.environ.get('NOTIFICATION_MAIL_PASSWORD')
SUPPORT_MAIL_PASSWORD = os.environ.get('SUPPORT_MAIL_PASSWORD')

DATABASE_URL = f'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
IMAGE_FOLDER = 'app/web/view/static/user_images'
