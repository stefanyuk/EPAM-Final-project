import re
from config import Config
from flask import Blueprint, current_app, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.exceptions import HTTPException, InternalServerError


errors = Blueprint('errors', __name__)


@errors.app_errorhandler(HTTPException)
def http_error(error):
    if check_api_version():
        return {
            'status': 410,
            'message': 'You are using not the current version of api.' +
                       f' Please use the newest version which is {Config.API_VERSION}',
            'correct_url': f'/api/v{Config.API_VERSION}/...'
        }, 410

    return {
        'code': error.code,
        'message': error.name,
        'description': error.description,
    }, error.code


@errors.app_errorhandler(IntegrityError)
def sqlalchemy_integrity_error(error):
    return {
        'code': 400,
        'message': 'Database integrity error',
        'description': str(error.orig),
    }, 400


@errors.app_errorhandler(SQLAlchemyError)
def sqlalchemy_error(error):
    if current_app.config['DEBUG'] is True:
        return {
            'code': InternalServerError.code,
            'message': 'Database error',
            'description': str(error),
        }, 500
    else:
        return {
            'code': InternalServerError.code,
            'message': InternalServerError().name,
            'description': InternalServerError.description,
        }, 500


def check_api_version():
    """
    Performs verification of the API version used by client in case if "NOT FOUND" exception occurs

    :return: error message that will be showed to the client
    """
    p = re.compile(r'/api/v1')
    path = request.path

    if not p.search(path):
        return True
    else:
        return {
            'status': 410,
            'message': 'You are using not the current version of api.' +
                       f' Please use the newest version which is {Config.API_VERSION}',
            'correct_url': f'/api/v{Config.API_VERSION}/...'
        }