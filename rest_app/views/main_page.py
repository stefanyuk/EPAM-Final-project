from flask import Blueprint, render_template, url_for
from rest_app.forms.personal_info_forms import UpdateProfileForm, AddressForm, populate_form_values
from flask_login import current_user, login_required
from rest_app.models import User, Address

wlc = Blueprint('wlc', __name__)


@wlc.route('/')
def welcome_landing():
    login_url = url_for('auth.login')
    log_out_url = url_for('auth.logout')
    register_url = url_for('auth.register')
    return render_template(
        'welcome_landing.html',
        login_url=login_url,
        log_out_url=log_out_url,
        register_url=register_url
    )
