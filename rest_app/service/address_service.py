from uuid import uuid4
from flask_restful import reqparse
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


def address_data_parser():
    parser = reqparse.RequestParser()
    
    parser.add_argument('city', type=str, help='you did not provide city name')
    parser.add_argument('street', type=str, help='you did not provide name of the street')
    parser.add_argument('street_number', type=str, help='you did not provide number of the street')
    parser.add_argument('postal_code', type=str, help='you did not provide postal code')
    parser.add_argument('user_id', type=str, help='you did not provide user id')

    return parser

