from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False   


class HerokuConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ['HEROKU_POSTGRESQL_BLUE_URL']


class TestingConfig(Config):
    database_name = "capstone_test"
    database_path = "postgres://{}/{}".format('localhost:5432', database_name)

    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = database_path

class LocalConfig(Config):
    database_name = "capstone"
    database_path = "postgres://{}/{}".format('localhost:5432', database_name)

    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = database_path