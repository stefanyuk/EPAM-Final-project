from sqlalchemy import func, asc, desc
from flask import request
from uuid import uuid4
from rest_app import db
from rest_app.models import EmployeeInfo
from rest_app.models.common import Common


class Department(Common, db.Model):
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

    @staticmethod
    def verify_colum_name(col_name):
        if col_name not in ['name', 'average_salary', 'total_employees']:
            col_name = 'name'

        return col_name

    @classmethod
    def sort_by_column(cls):
        order = []
        i = 0
        while True:
            col_index = request.args.get(f'order[{i}][column]')
            if col_index is None:
                break
            col_name = cls.verify_colum_name(request.args.get(f'columns[{col_index}][data]'))
            if col_name == 'total_employees':
                return cls.sort_by_total_employees(i)
            descending = request.args.get(f'order[{i}][dir]') == 'desc'
            col = getattr(cls, col_name)
            if descending:
                col = col.desc()
            order.append(col)
            i += 1

        return order

    @classmethod
    def sort_by_total_employees(cls, index):
        order = desc if request.args.get(f'order[{index}][dir]') == 'desc' else asc
        subquery = db.session.query(Department.id.label('department_id'), func.count(EmployeeInfo.id)\
                                    .label('total_employees')) \
            .outerjoin(EmployeeInfo) \
            .group_by(Department.id).subquery(name='sub')
        query = db.session.query(Department.id, Department.name, subquery.c.total_employees) \
            .join(subquery, Department.id == subquery.c.department_id) \
            .order_by(order(subquery.c.total_employees))

        return query

    @classmethod
    def table_search(cls, query, search):
        """Performs a search on the name field of the Department table according to the provided data"""
        query = query.filter(Department.name.like(f'%{search}%'))

        return query

    def __repr__(self):
        return f'<Department {self.name}>'
