from sqlalchemy import func
from uuid import uuid4
from rest_app import db
from rest_app.models import EmployeeInfo
from rest_app.models.common import Common


class DepartmentSearch():

    @staticmethod
    def verify_colum_name(col_name):
        if col_name not in ['name', 'average_salary', 'total_employees']:
            col_name = 'name'

        return col_name

    @classmethod
    def sort_by_total_employees(cls, order):
        """
        Creates a query that sorts a total employees column
        of the Department table in a specified order
        """
        query = db.session.query(Department.id, Department.name, func.count(EmployeeInfo.id).label('total_employees')) \
            .outerjoin(EmployeeInfo) \
            .group_by(Department.id) \
            .order_by(order('total_employees'))

        return query

    @classmethod
    def sort_by_average_salary(cls, order):
        """
        Creates a query that sorts an average salary column
        of the Department table in a specified order
        """
        query = db.session.query(Department.id, Department.name, func.avg(EmployeeInfo.salary).label('average_salary')) \
            .outerjoin(EmployeeInfo) \
            .group_by(Department.id) \
            .order_by(order('average_salary'))

        return query

    @classmethod
    def table_search(cls, query, search):
        """Performs a search on the name field of the Department table according to the provided data"""
        query = query.filter(cls.name.like(f'%{search}%'))

        return query


class Department(Common, DepartmentSearch, db.Model):
    __tablename__ = 'department'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.Text, nullable=True)
    employees = db.relationship('EmployeeInfo', backref='department', lazy='dynamic')

    @classmethod
    def create(cls, **kwargs):
        """Creates new department"""
        dept = cls(id=str(uuid4()), **kwargs)
        db.session.add(dept)
        db.session.commit()
        return dept

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
