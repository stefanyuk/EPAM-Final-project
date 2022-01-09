from .department_view import department
from .employee_view import employee
from .orders_view import order
from .user_view import user
from .admin_views import admin
from .main_page import wlc
from .auth import auth


def register_view_blueprints(app):
    app.register_blueprint(department)
    app.register_blueprint(employee)
    app.register_blueprint(order)
    app.register_blueprint(user)
    app.register_blueprint(admin)
    app.register_blueprint(wlc)
    app.register_blueprint(auth)
