from apifairy import body, response, other_responses, authenticate
from flask import Blueprint
from rest_app.api.auth import token_auth
from rest_app.models import EmployeeInfo
from rest_app.schemas import EmployeeSchema, EmployeeCreateSchema

employees = Blueprint('employees', __name__, url_prefix='/api/v1')

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


@employees.route('/employees', methods=['GET'])
@authenticate(token_auth)
@response(employees_schema)
def get_all():
    """Retrieve all employees"""
    return EmployeeInfo.query.all()


@employees.route('/employees', methods=['POST'])
@authenticate(token_auth)
@body(EmployeeCreateSchema())
@response(employee_schema, status_code=201, description='Employee was created')
def new(args):
    """Create new employee"""
    return EmployeeInfo.create(**args)


@employees.route('/employees/<string:employee_id>', methods=['GET'])
@authenticate(token_auth)
@response(employee_schema)
@other_responses({404: 'Employee not found'})
def get(employee_id):
    """Retrieve employee by id"""
    return EmployeeInfo.query.get_or_404(employee_id)


@employees.route('/employees/<string:employee_id>', methods=['PATCH'])
@authenticate(token_auth)
@body(EmployeeSchema(partial=True))
@response(employee_schema)
@other_responses({404: 'Employee not found'})
def update(args, employee_id):
    """Update employee information"""
    EmployeeInfo.query.get_or_404(employee_id)
    return EmployeeInfo.update(employee_id, args)


@employees.route('/employees/<string:employee_id>', methods=['DELETE'])
@authenticate(token_auth)
@other_responses({204: 'No content'})
def delete(employee_id):
    """Delete category"""
    EmployeeInfo.delete(employee_id)
    return '', 204
