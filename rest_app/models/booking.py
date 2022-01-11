from rest_app import db


class Booking(db.Model):
    __tablename__ = 'booking'

    id = db.Column(db.String, primary_key=True)
    table_id = db.Column(db.ForeignKey('table.id', ondelete='SET NULL'))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.ForeignKey('user.id', ondelete='SET NULL'))
