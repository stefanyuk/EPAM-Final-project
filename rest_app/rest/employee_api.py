from sqlalchemy import exc
from flask import jsonify
from flask_restful import Resource
from rest_app.service.employee_service import *
from rest_app.error_services.error_messages import error_employee_not_found
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
        employees = get_all_rows_from_db(EmployeeInfo)
        employee_list = [employee_data_to_dict(employee) for employee in employees]

        return jsonify(employee_list)

    def post(self):
        """
        Creates a new employee in the database
        """
        args = employee_data_parser().parse_args()
        employee_id = add_employee(**args)

        return {'message': f'employee with id - {employee_id} - has been created'}, 201

    def delete(self):
        """
        Deletes all employees from the database
        """
        delete_all_rows_from_db(EmployeeInfo)

        return {'message': 'all employees were deleted from the database'}


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
            return error_employee_not_found, 404

        return employee_data_to_dict(employee)

    def put(self, employee_id):
        """
        Updates information about the specific employee in the database

        :param employee_id: id of the employee
        """
        args = employee_data_parser().parse_args()

        try:
            update_employee(employee_id, **args)
        except exc.NoResultFound:
            return error_employee_not_found, 404

        return {'message': f'employee - {employee_id} - has been updated'}

    def delete(self, employee_id):
        """
        Deletes specified employee from the database

        :param employee_id: id of the employee
        """
        try:
            delete_row_by_id(EmployeeInfo, employee_id)
        except exc.NoResultFound:
            return error_employee_not_found, 404

        return {'message': 'employee was deleted'}
