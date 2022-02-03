from marshmallow import validate, validates, ValidationError
from flask import request
import datetime as dt
from rest_app import ma
from rest_app.models import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field(required=True, validate=validate.Length(min=3, max=64))
    password = ma.String(required=True, load_only=True, validate=validate.Length(min=5))
    registered_on = ma.auto_field(missing=dt.datetime.now().date())
    first_name = ma.auto_field(missing=None)
    last_name = ma.auto_field(missing=None)
    last_login_date = ma.auto_field(dump_only=True)
    email = ma.auto_field(required=True, validate=validate.Email())
    phone_number = ma.auto_field(missing=None)
    birth_date = ma.auto_field(missing=None)
    is_admin = ma.auto_field(missing=None)
    is_employee = ma.auto_field(missing=None)

    @validates('username')
    def validate_username(self, value):
        """Validates whether provided username does not exist and whether it starts with a letter"""
        if not value[0].isalpha():
            raise ValidationError('Username must start with a letter')
        if User.query.filter_by(username=value).first():
            raise ValidationError('Username already exists. Use a different username')

    @validates('email')
    def validate_email(self, value):
        """Validates whether provided email does not exist"""
        if User.query.filter_by(email=value).first():
            raise ValidationError('Email already exists. Use a different email')


class UpdateUserSchema(UserSchema):
    @validates('username')
    def validate_username(self, value):
        """Validates whether provided username does not exist and whether it starts with a letter"""
        user_id = request.path.split('/')[-1]
        user = User.query.get(user_id)
        if user:
            if value != user.username:
                if User.query.filter_by(username=value).first():
                    raise ValidationError('Username already exists. Use a different username')

    @validates('email')
    def validate_email(self, value):
        """Validates whether provided email does not exist"""
        user_id = request.path.split('/')[-1]
        if value != User.query.get(user_id).email:
            if User.query.filter_by(email=value).first():
                raise ValidationError('Email already exists. Use a different email')
