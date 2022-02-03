from marshmallow import EXCLUDE
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from rest_app.forms.auth_forms import RegistrationForm, LoginForm
from rest_app.models import User
from rest_app.schemas import UserSchema
from flask_login import login_user, current_user, logout_user

auth = Blueprint('auth', __name__)
user_schema = UserSchema(partial=True, unknown=EXCLUDE)


@auth.route('/register', methods=('GET', 'POST'))
def register():
    """Handles user registration process"""
    if current_user.is_authenticated:
        return redirect(url_for('wlc.welcome_landing'))

    form = RegistrationForm()

    if form.validate_on_submit():
        data = user_schema.load(form.data)
        user = User.create(**data)
        login_user(user)
        return redirect(url_for('shop.welcome_landing'))

    return render_template('register.html', form=form)


@auth.route('/login', methods=('GET', 'POST'))
def login():
    """Handles user authentication process"""
    if current_user.is_authenticated:
        return redirect(url_for('shop.welcome_landing'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            user.update_last_login_date()
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('shop.welcome_landing'))

        flash('Login unsuccessful. Please check your username and password', 'danger')

    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    """Handles user logout process and clears the session"""
    session.clear()
    logout_user()
    return redirect(url_for('shop.welcome_landing'))
