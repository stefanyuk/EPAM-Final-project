from uuid import uuid4
from flask_restful import reqparse
from rest_app.models import Category
from rest_app import db


def add_category(name):
    category = Category(
        id=str(uuid4()),
        name=name
    )

    db.session.add(category)
    db.session.commit()

    return category


def category_data_parser():
    """
    Parses category information needed for update
    """
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)

    return parser
