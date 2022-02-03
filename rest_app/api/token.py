from flask import Blueprint
from apifairy import authenticate, response, other_responses
from rest_app import db
from rest_app.api.auth import basic_auth
from rest_app.models import Token
from rest_app.schemas.token_schema import TokenSchema

tokens = Blueprint('tokens', __name__, url_prefix='/api/v1')
token_schema = TokenSchema()


@tokens.route('/tokens', methods=['POST'])
@authenticate(basic_auth)
@response(token_schema)
@other_responses({401: 'Invalid username or password'})
def new():
    """Create new access token"""
    user = basic_auth.current_user()
    token = user.generate_auth_token()
    db.session.add(token)
    Token.clean()  # keep token table clean of old tokens
    db.session.commit()
    return token
