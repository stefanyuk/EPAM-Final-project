import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base configuration"""
    DEBUG = False
    TESTING = False
    API_VERSION = 1


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    SECRET_KEY = 'dev'
    API_VERSION = 1
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://test:test@localhost:5432/restwebapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MIGRATION_DIR = os.path.join(basedir, 'my_app\migrations')


class TestingConfig(Config):
    """Testing Configuration"""

    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MIGRATION_DIR = os.path.join(basedir, 'my_app\migrations')
    API_VERSION = 1
