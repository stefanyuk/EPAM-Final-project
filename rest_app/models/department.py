from sqlalchemy import func
from rest_app import db
from rest_app.models import EmployeeInfo


class Department(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.Text, nullable=True)
    employees = db.relationship('EmployeeInfo', backref='department', lazy='dynamic')

    def data_to_dict(self):
        """
        Serializer that returns a dictionary from department table fields
        """
        avg_salary = self.get_average_dept_salary()

        department_info = {
            'id': self.id,
            'name': self.name,
            'average_department_salary': 0 if isinstance(avg_salary, int) else str(avg_salary.one()['avg_salary']),
            'total_employees': self.get_total_employees(),
            'description': self.description
        }

        return department_info

    def get_average_dept_salary(self):
        """
        Get average department salary
        """
        dept_id = self.id

        if not self.employees.all():
            return 0

        query = db.session.query(Department.id, func.ROUND(func.AVG(EmployeeInfo.salary), 3).label('avg_salary')) \
            .outerjoin(EmployeeInfo) \
            .filter(Department.id == dept_id) \
            .group_by(Department.id)

        return query

    def get_total_employees(self):
        """
        Get total quantity of employees in the department
        """

        if not self.employees.all():
            return 0

        return len(self.employees.all())

    def __repr__(self):
        return f'<Department {self.name}>'
