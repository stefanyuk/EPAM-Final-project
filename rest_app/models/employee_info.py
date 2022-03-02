from uuid import uuid4
from rest_app import db
from rest_app.models.common import Common
from rest_app.models import User


class EmployeeSearch():

    @staticmethod
    def verify_colum_name(col_name):
        if col_name not in ['first_name', 'last_name', 'hire_date', 'salary', 'department_name']:
            col_name = 'first_name'

        return col_name

    @classmethod
    def sort_by_first_name(cls, order):
        subquery = db.session.query(User.id.label('user_id'), User.first_name, User.last_name).subquery(name='sub')
        query = db.session.query(EmployeeInfo) \
            .join(subquery, EmployeeInfo.user_id == subquery.c.user_id) \
            .order_by(order(subquery.c.first_name))

        return query

    @classmethod
    def sort_by_last_name(cls, order):
        subquery = db.session.query(User.id.label('user_id'), User.first_name, User.last_name).subquery(name='sub')
        query = db.session.query(EmployeeInfo) \
            .join(subquery, EmployeeInfo.user_id == subquery.c.user_id) \
            .order_by(order(subquery.c.last_name))

        return query

    @classmethod
    def table_search(cls, query, search):
        """Performs a search on the specific fields of the User table according to the provided data"""
        from rest_app.models import Department

        query = db.session.query(
            EmployeeInfo.id, EmployeeInfo.user_id, User.first_name, User.last_name, EmployeeInfo.salary,
            EmployeeInfo.hire_date, Department.name, EmployeeInfo.available_holidays
        ) \
            .join(Department) \
            .join(User) \
            .filter(
            db.or_(
                User.first_name.like(f'%{search}%'),
                User.last_name.like(f'%{search}%'),
                Department.name.like(f'%{search}%')
            )
        )

        return query


class EmployeeInfo(Common, EmployeeSearch, db.Model):
    __tablename__ = 'employee_info'

    id = db.Column(db.String, primary_key=True)
    hire_date = db.Column(db.Date)
    department_id = db.Column(db.ForeignKey('department.id', ondelete='SET NULL'))
    salary = db.Column(db.Numeric(10, 3), nullable=False)
    user_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    available_holidays = db.Column(db.Integer)

    @classmethod
    def create(cls, **kwargs):
        """Creates new employee"""
        employee = cls(id=str(uuid4()), **kwargs)
        db.session.add(employee)
        db.session.commit()
        return employee

    @property
    def first_name(self):
        return self.user.first_name

    @first_name.setter
    def first_name(self, value):
        self.user.first_name = value

    @property
    def last_name(self):
        return self.user.last_name

    @last_name.setter
    def last_name(self, value):
        self.user.last_name = value

    def __repr__(self):
        return f'<Employee {self.user.first_name} {self.user.last_name}>'
