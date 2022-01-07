from sqlalchemy import exc
from flask import jsonify
from flask_restful import Resource
from rest_app.service.vacation_service import *
from rest_app.service.common_services import *
from rest_app.errors.error_messages import record_not_found_by_id_error
from rest_app.rest.auth import auth
from rest_app.models import Vacation


class VacationsAPI(Resource):
    """
    Resource that handles HTTP requests related to all vacations registered in the database
    """
    decorators = [auth.login_required]

    def get(self):
        """
        Returns list of all vacations
        """
        vacations = get_all_rows_from_db(Vacation)
        vacations_list = [vacation_data_to_dict(vacation) for vacation in vacations]

        return jsonify(vacations_list)

    def post(self):
        """
        Creates a new vacation record in the database
        """
        args = vacation_data_parser().parse_args()
        vacation_id = add_vacation(**args)

        return {'message': f'vacation with id - {vacation_id} - has been created'}, 201


class VacationAPI(Resource):
    """
    Resource that handles HTTP requests related to the specific vacation in the database
    """
    decorators = [auth.login_required]

    def get(self, vacation_id):
        """
        Returns vacation with the specified id

        :param vacation_id: unique id that identifies vacation
        """
        try:
            vacation = get_row_by_id(Vacation, vacation_id)
        except exc.NoResultFound:
            return record_not_found_by_id_error('vacation'), 404

        return vacation_data_to_dict(vacation)

    def put(self, vacation_id):
        """
        Updates information about the specific vacation in the database

        :param vacation_id: unique id that identifies vacation
        """
        args = vacation_data_parser().parse_args()

        try:
            update_vacation(vacation_id, **args)
        except exc.NoResultFound:
            return record_not_found_by_id_error('vacation'), 404

        return {'message': f'vacation - {vacation_id} - has been updated'}

    def delete(self, vacation_id):
        """
        Deletes specified vacation from the database

        :param vacation_id: unique id that identifies vacation
        """
        delete_row_by_id(Vacation, vacation_id)

        return '', 204