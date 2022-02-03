from uuid import uuid4
from rest_app import db
from rest_app.models.common import Common


class EmployeeInfo(Common, db.Model):
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

    def __repr__(self):
        return f'<Employee {self.user.first_name} {self.user.last_name}>'
