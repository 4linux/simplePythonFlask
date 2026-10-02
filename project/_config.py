import os
from urllib.parse import quote_plus

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'emeW7Bb48Wai6SIiVIorvn+SsHM=')

APP_VERSION = os.environ.get('APP_VERSION', 'dev')

DB_HOST = os.environ.get('DB_HOST', 'mariadb')
DB_PORT = os.environ.get('DB_PORT', '3306')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'qwe123qwe')
DB_NAME = os.environ.get('DB_NAME', 'simplePythonFlask')

# DATABASE_URL, quando definida, tem prioridade sobre as variaveis DB_*
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL',
    'mysql+pymysql://%s:%s@%s:%s/%s' % (
        DB_USER, quote_plus(DB_PASSWORD), DB_HOST, DB_PORT, DB_NAME))
SQLALCHEMY_TRACK_MODIFICATIONS = False
