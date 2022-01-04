from flask import Blueprint, request
from flask_restful import Api
import re
from rest_app.rest.employee_api import EmployeesAPI, EmployeeAPI
from rest_app.rest.department_api import DepartmentAPI, DepartmentsAPI
from rest_app.rest.order_api import OrdersAPI, OrderAPI
from rest_app.rest.user_api import UsersAPI, UserAPI
from rest_app.rest.vacation_api import VacationAPI, VacationsAPI
from rest_app.error_services.error_output import generate_error_message
from rest_app.error_services.error_messages import error_bad_api_version, error_for_not_found


rp_api = Blueprint('rp_api', __name__, url_prefix='/api/v1')

api = Api(rp_api)

api.add_resource(EmployeesAPI, '/employees', endpoint='employee_list')
api.add_resource(EmployeeAPI, '/employees/<employee_id>', endpoint='employee')
api.add_resource(DepartmentsAPI, '/departments', endpoint='department_list')
api.add_resource(DepartmentAPI, '/departments/<string:department_id>', endpoint='department')
api.add_resource(OrdersAPI, '/orders', endpoint='order_list')
api.add_resource(OrderAPI, '/orders/<string:order_id>', endpoint='order')
api.add_resource(UsersAPI, '/users', endpoint='user_list')
api.add_resource(UserAPI, '/users/<string:user_id>', endpoint='user')
api.add_resource(VacationsAPI, '/vacations', endpoint='vacation_list')
api.add_resource(VacationAPI, '/vacations/<string:vacation_id>', endpoint='vacation')


@rp_api.errorhandler(404)
def check_api_version(e):
    """
    Handler that performs verification of the API version used by client in case if exception occurs

    :param e: exception name
    :return: error message that will be showed to the client
    """
    p = re.compile(r'/api/v1')
    path = request.path

    if path.replace('/', ''):
        if not p.search(path):
            return generate_error_message(error_bad_api_version, error_code=410)

    return generate_error_message(error_for_not_found)
