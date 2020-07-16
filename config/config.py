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
    SQLALCHEMY_DATABASE_URI = 'postgres://rpqukyrwefnexz:a2c8e358006e2915ca776dd18ca4ae79a7192cb108aa8ee95805ff1abec0645a@ec2-34-202-7-83.compute-1.amazonaws.com:5432/d1t170ta0skouh'


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