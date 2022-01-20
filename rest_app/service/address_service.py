from uuid import uuid4
from flask_restful import reqparse
from sqlalchemy import and_
from flask_login import current_user
from rest_app.models import Address
from rest_app import db
from rest_app.service.common_services import set_all_parser_args_to_unrequired


def add_address(user_id, city, postal_code, street, street_number):
    """
    Creates new address record in the database
    :param user_id: id of the user to which this address belongs
    :return:
    """
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


def address_data_parser():
    """
    Creates a parser to parse information for address creation
    """
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
    """
    Creates a parser to parse address information from the form
    """
    parser = address_data_parser().copy()
    parser.remove_argument('user_id')

    return set_all_parser_args_to_unrequired(parser)


def check_if_address_exists(address_form):
    """
    Verifies whether address already exists in the list
    of addresses of the specified user
    """
    query = Address.query.filter(
        and_(
            Address.user_id == current_user.id,
            Address.street == address_form.street.data,
            Address.street_number == str(address_form.street_number.data)
        )
    )

    return query
