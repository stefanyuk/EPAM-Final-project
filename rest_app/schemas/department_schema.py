from marshmallow import post_dump, validates, ValidationError
from rest_app import ma
from rest_app.models import Department


class DepartmentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Department
        ordered = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    description = ma.auto_field()
    average_salary = ma.Decimal(dump_only=True)
    total_employees = ma.Int(dump_only=True)

    @validates('name')
    def validate_name(self, value):
        """Validates whether department with the provided name already exists"""
        department = Department.query.filter_by(name=value).first()

        if department:
            raise ValidationError('Department with this name already exists')

    @post_dump
    def add_average_salary_and_total_employees(self, data, **kwargs):
        """
        Calculates average salary and total employees for the department and
        adds it to the serialized Schema
        """
        if data.get('id'):
            dept = Department.query.get(data['id'])
            avg_salary = dept.get_average_dept_salary()
            data['average_salary'] = 0 if isinstance(avg_salary, int) else avg_salary.one()['avg_salary']
            data['total_employees'] = dept.get_total_employees()

        return data
