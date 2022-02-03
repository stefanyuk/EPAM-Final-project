from datetime import datetime, timedelta
from flask import current_app
import secrets
from rest_app import db


class Token(db.Model):
    __tablename__ = 'token'

    id = db.Column(db.String, primary_key=True)
    access_token = db.Column(db.String(64), nullable=False, unique=True)
    access_expiration = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    def generate(self):
        """Generates a new access token"""
        self.access_token = secrets.token_urlsafe()
        self.access_expiration = datetime.utcnow() + \
            timedelta(minutes=current_app.config['ACCESS_TOKEN_MINUTES'])

    @classmethod
    def clean(cls):
        """Remove any tokens that have been expired for more than a day"""
        yesterday = datetime.utcnow() - timedelta(days=1)
        tokens = cls.query.filter(cls.access_expiration < yesterday).all()

        for token in tokens:
            token.delete()
