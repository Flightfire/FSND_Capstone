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
    SQLALCHEMY_DATABASE_URI = 'postgres://caknuwumdnhotv: \
        f62e05a5f053a9dc285c19d0b1d44c67de283b1d05923b39f41f9607113082f7 \
        @ec2-34-197-188-147.compute-1.amazonaws.com:5432/ddebgjg37tjl5j'


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