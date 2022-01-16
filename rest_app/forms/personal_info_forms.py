from flask_wtf import FlaskForm
import phonenumbers
from wtforms import StringField, SubmitField, ValidationError, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Optional
from rest_app.models import User


class UpdateProfileForm(FlaskForm):
    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[Optional()])
    first_name = StringField('First Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[Optional()])
    birth_date = DateField(validators=[Optional()])

    submit_profile = SubmitField('Update')

    def validate_username(self, username):
        user = User.query.filter(User.id == self.user_id).first()

        if username.data != user.username:
            user = User.query.filter(User.username == username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter(User.id == self.user_id).first()

        if email.data != user.email:
            user = User.query.filter(User.email == email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

    def validate_phone_number(self, phone_number):
        try:
            p = phonenumbers.parse(phone_number.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')

    def change_user_form_values(self, user_id):
        user = User.query.filter(User.id == user_id).first()

        self.username.data = user.username
        self.email.data = user.email
        self.phone_number.data = user.phone_number
        self.first_name.data = user.first_name
        self.last_name.data = user.last_name
        self.birth_date.data = user.birth_date


class AddressForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    street_number = IntegerField('Street Number', validators=[DataRequired()])
    postal_code = StringField('Postal Code', validators=[DataRequired()])
    submit_address = SubmitField('Update')

    def change_address_values(self, address):
        self.city.data = address.city
        self.street.data = address.street
        self.street_number.data = address.street_number
        self.postal_code.data = address.postal_code
