from flask import Blueprint, render_template, url_for

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


@wlc.route('/nav')
def check_nav():
    return render_template('nav_bar.html')