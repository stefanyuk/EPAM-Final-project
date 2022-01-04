from rest_app import db


class Department(db.Model):
    __tablename = 'department'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.Text, nullable=True)
    employees = db.relationship('EmployeeInfo', backref='department', lazy='dynamic')
