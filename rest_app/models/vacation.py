from rest_app import db


class Vacation(db.Model):
    __tablename = 'vacation'

    id = db.Column(db.String, primary_key=True)
    employee_id = db.Column(db.ForeignKey('employee_info.id', ondelete='CASCADE'))
    vacation_start = db.Column(db.Date)
    vacation_end = db.Column(db.Date)
