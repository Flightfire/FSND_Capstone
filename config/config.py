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
    SQLALCHEMY_DATABASE_URI = 'postgres://mevbyboisflhuq:b9c9ced992f351ef3bfbf89f8ceae103bba9da91a97cfcddd95fc8dedd546de6@ec2-54-161-208-31.compute-1.amazonaws.com:5432/dr3qdbni44hkv'


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