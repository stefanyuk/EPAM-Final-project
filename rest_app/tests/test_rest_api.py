from rest_app import db


def test_my(client):
    print('Mu test')
    print(db.metadata.tables.keys())


def test_second(client):
    print('second')


def test_third(client):
    print('second')
