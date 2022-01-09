from flask import Blueprint, render_template, url_for
from rest_app.forms.personal_info_forms import UpdateProfileForm, AddressForm
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


@wlc.route('/personal_info')
@login_required
def profile():
    address =
    profile_form = UpdateProfileForm()
    address_form = AddressForm()
    profile_form.username.data = current_user.username
    profile_form.email.data = current_user.email
    address_form.city.data = address.city
    address_form.street.data = address.street
    address_form.street_number.data = address.street_number
    address_form.postal_code.data = address.postal_code

    return render_template(
        'personal_info.html',
        profile_form=profile_form,
        address_form=address_form,
        address=address
    )
