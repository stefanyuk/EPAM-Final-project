import pytest
from rest_app import create_app, db
from rest_app.database import create_superuser
from config import TestingConfig
from rest_app.tests.create_test_data_for_db import main


@pytest.fixture()
def app(postgresql):
    TestingConfig.SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}' + \
                                            f':{postgresql.info.port}/{postgresql.info.dbname}'
    app = create_app(test_config=TestingConfig)

    return app


@pytest.fixture(autouse=True)
def add_test_data(app):
    with app.app_context():
        db.create_all()

    main(db.session)
    create_superuser()


