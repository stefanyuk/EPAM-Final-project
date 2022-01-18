from .department_view import department
from .employee_view import employee
from .orders_view import order
from .user_view import user
from .admin_views import admin
from .auth import auth
from .shopping import shopping
from .product_views import product


def register_view_blueprints(app):
    """
    Registers all view blueprints in the Flask app
    :param app: Flask application
    """
    app.register_blueprint(department)
    app.register_blueprint(employee)
    app.register_blueprint(order)
    app.register_blueprint(user)
    app.register_blueprint(admin)
    app.register_blueprint(auth)
    app.register_blueprint(shopping)
    app.register_blueprint(product)
