from flask import Blueprint
from flask_restful import Api
from rest_app.rest.employee_api import EmployeesAPI, EmployeeAPI
from rest_app.rest.department_api import DepartmentAPI, DepartmentsAPI
from rest_app.rest.order_api import OrdersAPI, OrderAPI
from rest_app.rest.user_api import UsersAPI, UserAPI
from rest_app.rest.vacation_api import VacationAPI, VacationsAPI


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
