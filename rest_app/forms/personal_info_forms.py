from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email
from rest_app.models import User


class UpdateProfileForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter(User.username == username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(User.email == email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class AddressForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    street_number = StringField('Street Number', validators=[DataRequired()])
    postal_code = StringField('Postal Code', validators=[DataRequired()])
    submit = SubmitField('Update')
