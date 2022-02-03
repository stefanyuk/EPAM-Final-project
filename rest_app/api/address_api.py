from apifairy import body, response
from apifairy.decorators import other_responses
from flask import Blueprint, abort
from rest_app import db
from rest_app.models import Address
from rest_app.schemas.address_schema import AddressSchema

addresses = Blueprint('addresses', __name__, url_prefix='/api/v1')

address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)


@addresses.route('/addresses', methods=['POST'])
@body(address_schema)
@response(address_schema, status_code=201, description='address was created')
def new(args):
    """Create a new address"""
    address = Address.create(**args)
    db.session.add(address)
    db.session.commit()

    return address


@addresses.route('/addresses', methods=['GET'])
@response(addresses_schema)
def get_all():
    """Retrieve all addresses"""
    return Address.query.all()


@addresses.route('/addresses/<string:address_id>', methods=['GET'])
@response(address_schema)
@other_responses({404: 'address not found'})
def get(address_id):
    """Retrieve an address by id"""
    return Address.query.get_or_404(address_id)


@addresses.route('/addresses/<string:address_id>', methods=['PATCH'])
@body(AddressSchema(partial=True))
@response(address_schema)
@other_responses({404: 'Address not found'})
def update(args, address_id):
    """Update an address"""
    address = Address.query.get_or_404(address_id)
    address.update(args)
    return address


@addresses.route('/addresses/<string:address_id>', methods=['DELETE'])
@other_responses({204: 'No content'})
def delete(address_id):
    """Delete address"""
    db.session.query(Address).filter_by(id=address_id).delete()
    db.session.commit()
    return '', 204
