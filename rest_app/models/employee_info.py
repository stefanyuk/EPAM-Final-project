from rest_app import db


class EmployeeInfo(db.Model):
    __tablename__ = 'employee_info'

    id = db.Column(db.String, primary_key=True)
    hire_date = db.Column(db.Date)
    department_id = db.Column(db.ForeignKey('department.id', ondelete='SET NULL'))
    salary = db.Column(db.Numeric(10, 3))
    user_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE'))
    available_holidays = db.Column(db.Integer)
    vacations = db.relationship('Vacation', backref='employee', lazy='dynamic', passive_deletes=True)
