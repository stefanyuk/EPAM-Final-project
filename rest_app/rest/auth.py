from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from rest_app.models import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username and password:
        user = User.query.filter(User.username == username).first()

        if user and check_password_hash(user.password_hash, password):
            if user.is_admin:
                return user
