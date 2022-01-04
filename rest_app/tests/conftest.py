import pytest
from rest_app import create_app, db
from config import TestingConfig
import psycopg2
import os
from rest_app.models import User, Product, Department


@pytest.fixture
def app(postgresql):
    TestingConfig.SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{postgresql.info.user}:' + \
                                            f'@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}'
    app = create_app(test_config=TestingConfig)

    return app


@pytest.fixture(autouse=True)
def add_test_data(app, postgresql):
    with app.app_context():
        db.create_all()

    for file in next(os.walk('db_schemas'))[2]:
        with postgresql.cursor() as cur:
            cur.execute(open(f'db_schemas/{file}', "r").read())

    with postgresql.cursor() as cur:
        cur.execute("SELECT * FROM department")
        res = cur.fetchall()

    print('im done')