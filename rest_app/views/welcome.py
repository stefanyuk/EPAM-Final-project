from flask import Blueprint, render_template, request, redirect, url_for, flash

wlc = Blueprint('welcome', __name__)


@wlc.route('/')
def welcome_landing():
    return render_template('welcome_landing.html')
