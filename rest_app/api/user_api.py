from apifairy import body, response, authenticate
from apifairy.decorators import other_responses
from flask import Blueprint
from rest_app import db
from rest_app.schemas import UserSchema, AddressSchema, OrderSchema, UpdateUserSchema
from rest_app.models import User
from rest_app.api.auth import token_auth

users = Blueprint('users', __name__, url_prefix='/api/v1')
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@users.route('/users', methods=['POST'])
@authenticate(token_auth)
@body(user_schema)
@response(user_schema, status_code=201, description='User was created')
def new(args):
    """Create a new user"""
    return User.create(**args)


@users.route('/users', methods=['GET'])
@authenticate(token_auth)
@response(users_schema)
def get_all():
    """Retrieve all users"""
    return User.query.all()


@users.route('/users/<uuid:user_id>', methods=['GET'])
@authenticate(token_auth)
@response(user_schema)
@other_responses({404: 'User not found'})
def get(user_id):
    """Retrieve a user by id"""
    return User.query.get_or_404(str(user_id))


@users.route('/users/<string:username>', methods=['GET'])
@authenticate(token_auth)
@response(user_schema)
@other_responses({404: 'User not found'})
def get_by_username(username):
    """Retrieve a user by username"""
    return User.query.filter_by(username=username).first_or_404()


@users.route('/me', methods=['GET'])
@authenticate(token_auth)
@authenticate(token_auth)
@response(user_schema)
def me():
    """Retrieve the authenticated user"""
    return token_auth.current_user()


@users.route('/users/<string:user_id>/addresses')
@authenticate(token_auth)
@response(AddressSchema(many=True))
@other_responses({404: 'User not found'})
def addresses(user_id):
    """Retrieve all addresses of the specified user"""
    user = User.query.get_or_404(user_id)
    return user.addresses


@users.route('/users/<string:user_id>/orders')
@authenticate(token_auth)
@response(OrderSchema(many=True))
@other_responses({404: 'User not found'})
def orders(user_id):
    """Retrieve all orders of the specified user"""
    user = User.query.get_or_404(user_id)
    return user.orders


@users.route('/users/<string:user_id>', methods=['PATCH'])
@authenticate(token_auth)
@body(UpdateUserSchema(partial=True))
@response(user_schema)
@other_responses({404: 'User not found'})
def update(args, user_id):
    """Update user's information"""
    user = User.query.get_or_404(user_id)
    user.update(args)
    db.session.commit()
    return user


@users.route('/users/<string:users_id>', methods=['DELETE'])
@authenticate(token_auth)
@other_responses({204: 'No content'})
def delete(users_id):
    """Delete user"""
    User.query.get(users_id).delete()
    db.session.commit()
    return '', 204
