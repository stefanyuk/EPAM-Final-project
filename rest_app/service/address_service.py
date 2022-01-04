from uuid import uuid4
from rest_app.models import Address
from rest_app import db


def add_address(user_id, city, postal_code, street, street_number):
    address = Address(
        id=str(uuid4()),
        user_id=user_id,
        city=city,
        street=street,
        street_number=street_number,
        postal_code=postal_code,
    )

    db.session.add(address)
    db.session.commit()

