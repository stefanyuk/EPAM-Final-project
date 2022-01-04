from sqlalchemy import exc
from flask import jsonify
from flask_restful import Resource
from rest_app.service.department_service import *
from rest_app.service.common_services import *
from rest_app.error_services.error_messages import error_department_not_found
from rest_app.models import Department
from rest_app.rest.auth import auth


class DepartmentsAPI(Resource):
    """
    Resource that handles HTTP requests related to all departments registered in the database
    """
    decorators = [auth.login_required]

    def get(self):
        """
        Returns a list of all department in the database
        """
        departments = get_all_rows_from_db(Department)
        department_list = [department_data_to_dict(department) for department in departments]

        return jsonify(department_list)

    def post(self):
        """
        Creates new department in the database
        """
        args = department_data_parser().parse_args()
        new_dept_id = add_department(**args)

        return {'message': f'department with id - {new_dept_id} - has been created'}, 201

    def delete(self):
        """
        Deletes all departments from the database
        """
        delete_all_rows_from_db(Department)

        return {'message': 'all departments were deleted from the database'}


class DepartmentAPI(Resource):
    """
    Resource that handles HTTP requests related to the specific department in the database
    """
    decorators = [auth.login_required]

    def get(self, department_id):
        """
        Returns information about department with the specified name

        :param department_id: id of the department to be returned
        """
        try:
            department = get_row_by_id(Department, department_id)
        except exc.NoResultFound:
            return error_department_not_found, 404

        return department_data_to_dict(department)

    def put(self, department_id):
        args = department_data_parser().parse_args()

        try:
            update_department(department_id, **args)
        except exc.NoResultFound:
            return error_department_not_found, 404

        return {'message': 'department name was updated'}

    def delete(self, department_id):
        try:
            delete_row_by_id(Department, department_id)
        except exc.NoResultFound:
            return error_department_not_found, 404

        return {'message': 'department was deleted'}
