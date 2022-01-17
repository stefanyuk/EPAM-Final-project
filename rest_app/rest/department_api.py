from sqlalchemy import exc
from flask import jsonify
from flask_restful import Resource
from rest_app.service.department_service import *
from rest_app.service.common_services import *
from rest_app.errors.error_messages import record_not_found_by_id_error
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
        dept = Department.query.filter(Department.name == args['name']).first()

        if not dept:
            new_dept = add_department(**args)
            return {'message': f'department with id - {new_dept.id} - has been created'}, 201

        return {'message': 'Department already exists'}, 202


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
            return record_not_found_by_id_error('department'), 404

        return department_data_to_dict(department)

    def put(self, department_id):
        args = department_data_parser().parse_args()

        try:
            update_department_data(department_id, **args)
        except exc.NoResultFound:
            return record_not_found_by_id_error('department'), 404

        return {'message': f'department - {department_id} - has been updated'}

    def delete(self, department_id):
        delete_row_by_id(Department, department_id)

        return '', 204
