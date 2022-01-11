from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, DateField
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
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    birth_date = DateField(validators=[Optional()])

    submit = SubmitField('Update')

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


class AddressForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    street_number = StringField('Street Number', validators=[DataRequired()])
    postal_code = StringField('Postal Code', validators=[DataRequired()])
    submit = SubmitField('Update')


def add_values_to_address_form(address_form, address_object, user_id):
    address = address_object.query.filter(address_object.user_id == user_id).all()

    if address:
        address = address.pop()
        address_form.city.data = address.city
        address_form.street.data = address.street
        address_form.street_number.data = address.street_number
        address_form.postal_code.data = address.postal_code

    return address_form


def add_values_to_profile_form(profile_form, user_object, user_id):
    user = user_object.query.filter(user_object.id == user_id).first()

    profile_form.username.data = user.username
    profile_form.email.data = user.email
    profile_form.first_name.data = user.first_name
    profile_form.last_name.data = user.last_name
    profile_form.birth_date.data = user.birth_date

    return profile_form
