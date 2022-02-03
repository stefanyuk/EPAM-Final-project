from apifairy import body, response, other_responses
from flask import Blueprint
from rest_app import db
from rest_app.models import EmployeeInfo
from rest_app.schemas import EmployeeSchema, EmployeeCreateSchema

employees = Blueprint('employees', __name__, url_prefix='/api/v1')

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


@employees.route('/employees', methods=['GET'])
@response(employees_schema)
def get_all():
    """Retrieve all employees"""
    return EmployeeInfo.query.all()


@employees.route('/employees', methods=['POST'])
@body(EmployeeCreateSchema())
@response(employee_schema, status_code=201)
def new(args):
    """Create new employee"""
    return EmployeeInfo.create(**args)


@employees.route('/employees/<string:employee_id>', methods=['GET'])
@response(employee_schema)
@other_responses({404: 'Employee not found'})
def get(employee_id):
    """Retrieve employee by id"""
    return EmployeeInfo.query.get_or_404(employee_id)


@employees.route('/employees/<string:employee_id>', methods=['PATCH'])
@body(EmployeeSchema(exclude=('first_name', 'last_name'), partial=True))
@response(employee_schema)
@other_responses({404: 'Employee not found'})
def update(args, employee_id):
    """Update employee information"""
    employee = EmployeeInfo.query.get_or_404(employee_id)
    employee.update(args)
    return employee


@employees.route('/employees/<string:employee_id>', methods=['DELETE'])
@other_responses({204: 'No content'})
def delete(employee_id):
    """Delete category"""
    db.session.query(EmployeeInfo).filter_by(id=employee_id).delete()
    db.session.commit()
    return '', 204
