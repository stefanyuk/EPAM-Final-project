from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from rest_app.service.user_service import user_data_parser, update_user
from rest_app.forms.personal_info_forms import UpdateProfileForm, AddressForm

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/<string:user_id>')
@login_required
def user_detail(user_id):
    pass


@user.route('/create')
@login_required
def create_user():
    pass


@user.route('/<string:user_id>/update', methods=['POST'])
@login_required
def update_user(user_id):
    profile_form = UpdateProfileForm()

    if profile_form.validate_on_submit():
        args = user_data_parser().parse_args()
        update_user(user_id, **args)
        return redirect(url_for('wlc.profile'))

    return render_template('personal_info.html', profile_form=profile_form)


@user.route('/<string:user_id>/delete')
@login_required
def delete_user(user_id):
    pass