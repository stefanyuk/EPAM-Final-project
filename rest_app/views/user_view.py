from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from rest_app.service.user_service import form_user_data_parser, update_user, add_user
from rest_app.service.address_service import add_address
from rest_app.service.common_services import delete_row_by_id
from rest_app.forms.personal_info_forms import UpdateProfileForm, AddressForm, \
    add_values_to_address_form, add_values_to_profile_form
from rest_app.models import Address, User
from rest_app.forms.admin_forms import AddUser
from rest_app.views.admin_views import admin_or_user_required, admin_required

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/<string:user_id>')
@admin_or_user_required
@login_required
def user_detail(user_id):
    address_form = add_values_to_address_form(AddressForm(), Address, user_id)
    profile_form = add_values_to_profile_form(UpdateProfileForm(user_id), User, user_id)

    return render_template(
        'personal_info.html',
        profile_form=profile_form,
        address_form=address_form,
        user_id=user_id
    )


@user.route('/create', methods=['GET', 'POST'])
@admin_required
@login_required
def create_user():
    form = AddUser()

    if form.validate_on_submit():
        data = form_user_data_parser().parse_args()
        add_user(**data)
        flash('User was added successfully', 'success')
        return redirect(url_for('admin.admin_main'))

    form.phone_number.data = '+1'
    return render_template('add_user.html', form=form)


@user.route('/<string:user_id>/update', methods=['POST'])
@admin_or_user_required
@login_required
def update_user_values(user_id):
    profile_form = UpdateProfileForm(user_id)
    address_form = AddressForm()

    if profile_form.validate_on_submit():
        args = form_user_data_parser().parse_args()
        update_user(user_id, **args)
        flash('User information was updated', 'success')
        return redirect(url_for('user.user_detail', user_id=user_id))

    address_form = add_values_to_address_form(address_form, Address, user_id)
    profile_form = add_values_to_profile_form(profile_form, User, user_id)
    return render_template('personal_info.html', profile_form=profile_form, address_form=address_form)


@user.route('/<string:user_id>/delete')
@admin_required
@login_required
def delete_user(user_id):
    delete_row_by_id(User, user_id)
    flash('User was successfully deleted', 'success')
    return redirect(url_for('admin.admin_main'))


@user.route('/<string:user_id>/update_address', methods=['POST'])
@admin_or_user_required
@login_required
def update_address_details(user_id):
    profile_form = UpdateProfileForm(user_id)
    address_form = AddressForm()

    if address_form.validate_on_submit():
        add_address(
            user_id=user_id,
            city=address_form.city.data,
            postal_code=address_form.postal_code.data,
            street=address_form.street.data,
            street_number=address_form.street_number.data
        )
        flash('Address information has been updated', 'success')
        return redirect(url_for('user.user_detail', user_id=user_id))

    profile_form, address_form = populate_form_values(address_form, profile_form, user_id, Address, User)
    return render_template('personal_info.html', profile_form=profile_form, address_form=address_form)