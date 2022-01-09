from uuid import uuid4
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
