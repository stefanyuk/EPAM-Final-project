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

    return address


def address_data_to_dict(address):
    address_info = {
        'id': address.id,
        'city': address.city,
        'street': address.street,
        'street_number': address.street_number,
        'postal_code': address.postal_code
    }

    return address_info


def address_data_parser():
    parser = reqparse.RequestParser()

    parser.add_argument('city', type=str, help='you did not provide city name', required=True,
                        location=['json', 'form'])
    parser.add_argument('street', type=str, help='you did not provide name of the street', required=True,
                        location=['json', 'form'])
    parser.add_argument('street_number', type=str, help='you did not provide number of the street', required=True,
                        location=['json', 'form'])
    parser.add_argument('postal_code', type=str, help='you did not provide postal code', required=True,
                        location=['json', 'form'])
    parser.add_argument('user_id', type=str, help='you did not provide user id', required=True,
                        location=['json', 'form'])

    return parser


def address_data_form_parser():
    address_parser = address_data_parser().copy()

    address_parser.remove_argument('user_id')
    for arg in address_parser.args:
        arg.required = False

    return address_parser





# def address_data_form_parser():
#     parser = reqparse.RequestParser()
#
#     parser.add_argument('city', type=str, help='you did not provide city name',
#                         location='form')
#     parser.add_argument('street', type=str, help='you did not provide name of the street',
#                         location='form')
#     parser.add_argument('street_number', type=str, help='you did not provide number of the street',
#                         location='form')
#     parser.add_argument('postal_code', type=str, help='you did not provide postal code',
#                         location='form')
#     parser.add_argument('user_id', type=str, help='you did not provide user id',
#                         location='form')
#
#     return parser
