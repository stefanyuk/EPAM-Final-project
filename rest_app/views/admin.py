from flask import Blueprint, render_template
from flask_login import login_required

admin = Blueprint('admin', __name__)


@admin.route('/admin')
@login_required
def admin_main():
    return render_template('admin_main.html')
