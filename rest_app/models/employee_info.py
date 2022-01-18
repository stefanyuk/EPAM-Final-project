from rest_app import db


class EmployeeInfo(db.Model):
    __tablename__ = 'employee_info'

    id = db.Column(db.String, primary_key=True)
    hire_date = db.Column(db.Date)
    department_id = db.Column(db.ForeignKey('department.id', ondelete='SET NULL'))
    salary = db.Column(db.Numeric(10, 3), nullable=False)
    user_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    available_holidays = db.Column(db.Integer)

    def data_to_dict(self):
        """
        Serializer that returns a dictionary from employee table fields
        """
        employee_info = {
            'id': self.id,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'hire_date': str(self.hire_date),
            'department_name': self.department.name,
            'salary': str(self.salary),
            'available_holidays': self.available_holidays
        }

        return employee_info

    def __repr__(self):
        return f'<Employee {self.user.first_name} {self.user.last_name}>'
