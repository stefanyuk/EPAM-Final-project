from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from rest_app.forms.auth_forms import RegistrationForm, LoginForm
from rest_app.models import User
from rest_app.service.user_service import add_user, user_data_parser
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('wlc.welcome_landing'))

    form = RegistrationForm()

    if form.validate_on_submit():
        data = user_data_parser().parse_args()
        add_user(**data)
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('wlc.welcome_landing'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('shop.welcome_landing'))

        flash('Login unsuccessful. Please check your username and password', 'danger')

    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('shop.welcome_landing'))
