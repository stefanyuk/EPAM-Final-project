import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base configuration"""
    DEBUG = False
    TESTING = False
    API_VERSION = 1
    JSON_SORT_KEYS = False
    MIGRATION_DIR = os.path.join(basedir, 'my_app\migrations')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql+psycopg2://test:test@localhost:5432/restwebapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or '69d153ecbde99da143ee0e82d7794141'


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    SECRET_KEY = 'dev'


class TestingConfig(Config):
    """Testing Configuration"""

    TESTING = True
