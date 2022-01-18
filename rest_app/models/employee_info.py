from rest_app import db


class EmployeeInfo(db.Model):
    __tablename__ = 'employee_info'

    id = db.Column(db.String, primary_key=True)
    hire_date = db.Column(db.Date)
    department_id = db.Column(db.ForeignKey('department.id', ondelete='SET NULL'))
    salary = db.Column(db.Numeric(10, 3), nullable=False)
    user_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    available_holidays = db.Column(db.Integer)
