from marshmallow import validates, ValidationError, post_load, post_dump, pre_load
import datetime as dt
from uuid import uuid4
from rest_app import ma
from rest_app.models import EmployeeInfo, User, Department


class EmployeeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = EmployeeInfo
        ordered = True
        dateformat = '%Y-%m-%d'

    id = ma.auto_field(dump_only=True)
    hire_date = ma.auto_field(missing=dt.datetime.utcnow().date())
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    email = ma.String(dump_only=True)
    department_id = ma.auto_field(required=True, load_only=True)
    department = ma.Pluck('DepartmentSchema', 'name', dump_only=True)
    salary = ma.auto_field(required=True)
    available_holidays = ma.auto_field()
    user_id = ma.auto_field(required=False)

    @pre_load
    def add_department_id(self, data, **kwargs):
        """Adds department id to the load result in case if it was not provided"""
        if name := data.get('department'):
            data['department_id'] = Department.get_by_name(name).id
        return data

    @pre_load
    def exclude_unknown(self, data, **kwargs):
        """Excludes undesirable fields, that were provided in form"""
        unknown_fields = ['submit', 'update', 'csrf_token', 'department']
        data = {k: v for k, v in data.items() if k not in unknown_fields}
        return data

    @pre_load
    def convert_date_to_string(self, data, **kwargs):
        """Convert provided date to string in case if it's datetime object"""
        if date := data.get('hire_date'):
            if not isinstance(date, str):
                data['hire_date'] = dt.datetime.strftime(date, '%Y-%m-%d')

        return data

    @post_dump
    def add_user_info(self, data, **kwargs):
        """Adds name and surname to the result"""
        user = User.query.get(data['user_id'])
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['email'] = user.email
        return data

    @post_dump
    def add_department_name(self, data, **kwargs):
        """Adds department name to the result"""
        if not data.get('department'):
            user = User.query.get(data['user_id'])
            department = user.employee.department.name
            data['department'] = department

        return data

    @validates('user_id')
    def validate_user_id(self, value):
        """Validates provided user id"""
        if not User.query.get(value):
            raise ValidationError('User with the provided id does not exist')

    @validates('department_id')
    def validate_department_id(self, value):
        """Validates provided department id"""
        if not Department.query.get(value):
            raise ValidationError('Department with the provided id does not exist')


class EmployeeCreateSchema(EmployeeSchema):

    @post_load
    def create_employee_user(self, data, **kwargs):
        """Creates a default user account for the employee who does not have one"""
        first_name = data.pop('first_name')
        last_name = data.pop('last_name')
        if not data.get('user_id'):
            username = f'{last_name.lower()}.{str(uuid4())[:5]}'
            email = f'{first_name.lower()}.{last_name.lower()}.{str(uuid4())[:3]}@lacrema.com'
            password = '12345lacrema'
            user = User.create(
                username=username,
                email=email,
                password=password,
                first_name=first_name.capitalize(),
                last_name=last_name.capitalize(),
                is_employee=True
            )
            data['user_id'] = user.id
        return data
