import os
from decouple import config
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

uri = os.environ.get('DATABASE_URL') # or other relevant config var
if uri and uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1)

# reading env files
class Config:
    SECRET_KEY = config('SECRET_KEY','secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=40)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=40)
    JWT_SECERT_KEY = config('JWT_SECRET_KEY')

class DevConfig(Config):
    DEBUG = config('DEBUG', cast=bool)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = config('DEBUG', False, cast=bool)


# importing it to use for init.py file 
config_dict = {
    'dev':DevConfig,
    'prod':ProdConfig,
    'test':TestConfig,
}