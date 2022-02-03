from apifairy import body, response, other_responses, authenticate
from flask import Blueprint
from rest_app.api.auth import token_auth
from rest_app.models import Department
from rest_app.schemas import DepartmentSchema, EmployeeSchema

departments = Blueprint('departments', __name__, url_prefix='/api/v1')

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)


@departments.route('/departments', methods=['GET'])
@authenticate(token_auth)
@response(departments_schema)
def get_all():
    """Retrieve all departments"""
    return Department.query.all()


@departments.route('/departments', methods=['POST'])
@authenticate(token_auth)
@body(department_schema)
@response(department_schema, status_code=201, description='Department was created')
def new(args):
    """Create a new department"""
    return Department.create(**args)


@departments.route('/departments/<uuid:department_id>', methods=['GET'])
@authenticate(token_auth)
@response(department_schema)
@other_responses({404: 'Department not found'})
def get(department_id):
    """Retrieve department by id"""
    return Department.query.get_or_404(str(department_id))


@departments.route('/departments/<string:department_name>', methods=['GET'])
@authenticate(token_auth)
@response(department_schema)
@other_responses({404: 'Department not found'})
def get_by_name(department_name):
    """Retrieve department by name"""
    return Department.query.filter_by(name=department_name).first_or_404()


@departments.route('/departments/<uuid:department_id>/employees', methods=['GET'])
@authenticate(token_auth)
@response(EmployeeSchema(many=True))
@other_responses({404: 'Department not found'})
def get_department_employees_by_id(department_id):
    """Retrieve all employees who work in the specified department by department id"""
    department = Department.query.get_or_404(str(department_id))
    return department.employees


@departments.route('/departments/<string:department_name>/employees', methods=['GET'])
@authenticate(token_auth)
@response(EmployeeSchema(many=True))
@other_responses({404: 'Department not found'})
def get_department_employees_by_name(department_name):
    """Retrieve all employees who work in the specified department by department name"""
    department = Department.query.filter_by(name=department_name).first_or_404()
    return department.employees


@departments.route('/departments/<string:department_id>', methods=['PATCH'])
@authenticate(token_auth)
@body(department_schema)
@response(department_schema)
@other_responses({404: 'Department not found'})
def update(args, department_id):
    """Update department information"""
    Department.query.get_or_404(department_id)
    return Department.update(department_id, args)


@departments.route('/departments/<string:department_id>', methods=['DELETE'])
@authenticate(token_auth)
@other_responses({204: 'No content'})
def delete(department_id):
    """Delete department"""
    Department.delete(department_id)
    return '', 204
