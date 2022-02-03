from flask import Blueprint, render_template, redirect, url_for, flash
from marshmallow import EXCLUDE
from flask_login import login_required
from rest_app.schemas import UserSchema, AddressSchema, UpdateUserSchema
from rest_app.service.user_service import get_all_users_by_is_admin_filter
from rest_app.forms.personal_info_forms import UpdateProfileForm, AddressForm
from rest_app.models import Address, User
from rest_app.forms.admin_forms import AddUser
from rest_app.views.admin_views import admin_or_user_required, admin_required

user = Blueprint('user', __name__, url_prefix='/user')
user_schema = UserSchema(partial=True, unknown=EXCLUDE)
address_schema = AddressSchema(partial=True, unknown=EXCLUDE)
update_user_schema = UpdateUserSchema(partial=True, unknown=EXCLUDE)


@user.route('/<string:user_id>', methods=['GET', 'POST'])
@login_required
@admin_or_user_required
def user_detail(user_id):
    """Route that handles user data representation"""
    address_form = AddressForm()
    profile_form = UpdateProfileForm(user_id)
    populate_personal_info(address_form, profile_form, user_id)

    return render_template(
        'personal_info.html',
        profile_form=profile_form,
        address_form=address_form,
        user_id=user_id
    )


@user.route('/update_user/<string:user_id>', methods=['POST'])
def update_user_details(user_id):
    """Route that handles user data update"""
    address_form = AddressForm()
    profile_form = UpdateProfileForm(user_id)

    if profile_form.submit_profile.data and profile_form.validate():
        data = update_user_schema.load(profile_form.data)
        User.update(user_id, data)
        flash('User information was updated', 'success')
        return redirect(url_for('user.user_detail', user_id=user_id))
    elif address_form.submit_address.data and address_form.validate():
        data = address_schema.load(address_form.data)
        Address.create(user_id=user_id, **data)
        flash('Address information has been updated', 'success')
        return redirect(url_for('user.user_detail', user_id=user_id))

    populate_personal_info(address_form, profile_form, user_id)

    return render_template(
        'personal_info.html',
        profile_form=profile_form,
        address_form=address_form,
        user_id=user_id
    )


@user.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    """Route that handles user creation"""
    form = AddUser()

    if form.validate_on_submit():
        data = user_schema.load(form.data)
        User.create(**data)
        flash('User was successfully created', 'success')
        return redirect(url_for('admin.admin_main'))

    return render_template('add_user.html', form=form)


@user.route('/<string:user_id>/delete')
@login_required
@admin_required
def delete_user(user_id):
    """Route that handles user deletion"""
    user = User.query.filter_by(id=user_id).first()

    if not user.is_admin:
        User.delete(user_id)
        flash('User was successfully deleted', 'success')
    else:
        if len(get_all_users_by_is_admin_filter(True).all()) > 1:
            User.delete(user_id)
        else:
            flash('You are the only admin. Please create a new one and after repeat', 'danger')

    return redirect(url_for('admin.admin_main'))


def populate_personal_info(address_form, profile_form, user_id):
    """
    Pre-populates values in form fields

    :param address_form: instance of address from
    :param profile_form: instance of profile from
    :param user_id: unique id of the user
    """
    addresses = Address.query.filter(Address.user_id == user_id).all()

    if addresses:
        address_form.change_address_values(addresses.pop())

    profile_form.change_user_form_values(user_id)
