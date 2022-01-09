from sqlalchemy import exc
from flask import jsonify
from flask_restful import Resource
from rest_app.service.user_service import *
from rest_app.errors.error_messages import record_not_found_by_id_error
from rest_app.service.common_services import *
from rest_app.models import User
from rest_app.rest.auth import auth


class UsersAPI(Resource):
    """
    Resource that handles HTTP requests related to all users registered in the database
    """
    decorators = [auth.login_required]

    def get(self):
        """
        Returns list of all users
        """
        users = get_all_rows_from_db(User)
        users_list = [user_data_to_dict(user) for user in users]

        return jsonify(users_list)

    def post(self):
        """
        Creates a new user in the database
        """
        args = user_data_parser().parse_args()
        user = User.query.filter(User.username == args['username']).first()

        if not user:
            user = add_user(**args)
            return {'message': f'user with id - {user.id} - has been created'}, 201

        return {'message': 'User already exists'}, 202


class UserAPI(Resource):
    """
    Resource that handles HTTP requests related to the specific user in the database
    """
    decorators = [auth.login_required]

    def get(self, user_id):
        """
        Returns user with the specified id

        :param user_id: id of the user
        """
        try:
            user = get_row_by_id(User, user_id)
        except exc.NoResultFound:
            return record_not_found_by_id_error('user'), 404

        return user_data_to_dict(user)

    def put(self, user_id):
        """
        Updates information about the specific user in the database

        :param user_id: id of the employee
        """
        args = user_data_parser().parse_args()

        try:
            update_user(user_id, **args)
        except exc.NoResultFound:
            return record_not_found_by_id_error('user'), 404

        return {'message': f'user - {user_id} - has been updated'}

    def delete(self, user_id):
        """
        Deletes specified user from the database

        :param user_id: id of the user
        """
        delete_row_by_id(User, user_id)

        return '', 204
