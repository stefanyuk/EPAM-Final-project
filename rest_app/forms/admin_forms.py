from flask_wtf import FlaskForm
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from wtforms import TextAreaField, SubmitField, ValidationError, StringField, BooleanField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, Email
from rest_app.models import Department, User


class AddDepartment(FlaskForm):
    name = StringField('Department Name', validators=[DataRequired()])
    description = TextAreaField('Description')

    def validate_name(self, name):
        dept = Department.query.filter(Department.name == name).first()

        if dept:
            raise ValidationError('Department with this name already exists')


class AddEmployee(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    department = SelectField(
        'Department',
        choices=['1', '2', '3'],
        validators=[DataRequired()]
    )
    salary = FloatField('Salary', validators=[DataRequired()])
    submit = SubmitField('Add')


class AddUser(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=30)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[Length(min=12, max=12)])
    is_employee = BooleanField('Is employee?')
    is_admin = BooleanField('Is admin?')
    submit = SubmitField('Add')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter(User.email == email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_phone_number(self, phone_number):
        start = phone_number.data[:2]
        if start != '+1':
            raise ValidationError('Number should start with +1')
        try:
            p = phonenumbers.parse(phone_number.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')


