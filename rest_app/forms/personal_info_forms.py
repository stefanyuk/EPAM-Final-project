from flask_wtf import FlaskForm
from flask_login import current_user
import datetime
from wtforms import StringField, SubmitField, ValidationError, DateField
from wtforms.validators import DataRequired, Length, Email
from rest_app.models import User


class UpdateProfileForm(FlaskForm):
    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    first_name = StringField('First Name',
                             validators=[DataRequired()])
    last_name = StringField('Last Name',
                            validators=[DataRequired()])
    birth_date = DateField()

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


def populate_form_values(address_form, profile_form, user_id, address_object, user_object):
    address = address_object.query.filter(address_object.user_id == user_id).all()[-1]
    user = user_object.query.filter(user_object.id == user_id).first()

    profile_form = profile_form
    address_form = address_form
    profile_form.username.data = user.username
    profile_form.email.data = user.email
    profile_form.first_name.data = user.first_name
    profile_form.last_name.data = user.last_name
    profile_form.birth_date.data = user.birth_date

    if address:
        address_form.city.data = address.city
        address_form.street.data = address.street
        address_form.street_number.data = address.street_number
        address_form.postal_code.data = address.postal_code

    return profile_form, address_form
