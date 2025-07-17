import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
# print(basedir)

class Config:
    SECRET_KEY = "Some_password"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = os.environ.get('REDIS_URL')

class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'



