from sqlalchemy import exc
from flask import jsonify
from flask_restful import Resource
from rest_app.service.employee_service import *
from rest_app.errors.error_messages import record_not_found_by_id_error
from rest_app.service.common_services import *
from rest_app.rest.auth import auth


class EmployeesAPI(Resource):
    """
    Resource that handles HTTP requests related to all employees registered in the database
    """
    decorators = [auth.login_required]

    def get(self):
        """
        Returns list of all employees
        """
        employees = EmployeeInfo.query.all()
        employee_list = [employee.data_to_dict() for employee in employees]

        return jsonify(employee_list)

    def post(self):
        """
        Creates a new employee in the database
        """
        args = employee_data_parser().parse_args()
        employee = add_employee(**args)

        return {'message': f'employee with id - {employee.id} - has been created'}, 201


class EmployeeAPI(Resource):
    """
    Resource that handles HTTP requests related to the specific employee in the database
    """
    decorators = [auth.login_required]

    def get(self, employee_id):
        """
        Returns employee with the specified id

        :param employee_id: id of the employee
        """
        try:
            employee = get_row_by_id(EmployeeInfo, employee_id)
        except exc.NoResultFound:
            return record_not_found_by_id_error('employee'), 404

        return employee.data_to_dict()

    def patch(self, employee_id):
        """
        Updates information about the specific employee in the database

        :param employee_id: id of the employee
        """
        args = employee_update_data_parser().parse_args()

        try:
            update_employee_data(employee_id, **args)
        except exc.NoResultFound:
            return record_not_found_by_id_error('employee'), 404

        return {'message': f'employee - {employee_id} - has been updated'}

    def delete(self, employee_id):
        """
        Deletes specified employee from the database

        :param employee_id: id of the employee
        """
        delete_row_by_id(EmployeeInfo, employee_id)

        return '', 204
