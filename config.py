import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base configuration"""
    DEBUG = False
    TESTING = False
    API_VERSION = 1
    JSON_SORT_KEYS = False
    MIGRATION_DIR = os.path.join(basedir, 'my_app\migrations')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://test:test@localhost:5432/restwebapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    SECRET_KEY = 'dev'


class TestingConfig(Config):
    """Testing Configuration"""

    TESTING = True
