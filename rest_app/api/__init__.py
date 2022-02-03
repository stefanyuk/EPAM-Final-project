from rest_app.api.user_api import users
from rest_app.api.address_api import addresses
from rest_app.api.order_api import orders_api
from rest_app.api.products_api import products
from rest_app.api.category_api import categories
from rest_app.api.department_api import departments
from rest_app.api.employee_api import employees
from rest_app.api.token import tokens
# from rest_app.api.errors import api_errors


def register_api_blueprints(app):
    """
    Registers all api blueprints in the Flask app
    :param app: Flask application
    """
    app.register_blueprint(users)
    app.register_blueprint(addresses)
    app.register_blueprint(orders_api)
    app.register_blueprint(products)
    app.register_blueprint(categories)
    app.register_blueprint(employees)
    app.register_blueprint(departments)
    app.register_blueprint(tokens)
    # app.register_blueprint(api_errors)
