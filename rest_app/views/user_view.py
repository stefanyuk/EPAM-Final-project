from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from rest_app.service.user_service import form_user_data_parser, update_user, add_user
from rest_app.service.address_service import add_address, address_data_form_parser
from rest_app.service.common_services import delete_row_by_id
from rest_app.forms.personal_info_forms import UpdateProfileForm, AddressForm
from rest_app.models import Address, User
from rest_app.forms.admin_forms import AddUser
from rest_app.views.admin_views import admin_or_user_required, admin_required

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/<string:user_id>', methods=['GET', 'POST'])
@login_required
@admin_or_user_required
def user_detail(user_id):
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
    address_form = AddressForm()
    profile_form = UpdateProfileForm(user_id)

    if profile_form.submit_profile.data and profile_form.validate():
        args = form_user_data_parser().parse_args()
        update_user(user_id, **args)
        flash('User information was updated', 'success')
    elif address_form.submit_address.data and address_form.validate():
        args = address_data_form_parser().parse_args()
        add_address(user_id=user_id, **args)
        flash('Address information has been updated', 'success')

    populate_personal_info(address_form, profile_form, user_id)

    return redirect(url_for('user.user_detail', user_id=user_id))


@user.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    form = AddUser()

    if form.validate_on_submit():
        data = form_user_data_parser().parse_args()
        add_user(**data)
        flash('User was added successfully', 'success')
        return redirect(url_for('admin.admin_main'))

    form.phone_number.data = '+1'
    return render_template('add_user.html', form=form)


@user.route('/<string:user_id>/delete')
@login_required
@admin_required
def delete_user(user_id):
    delete_row_by_id(User, user_id)
    flash('User was successfully deleted', 'success')

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

