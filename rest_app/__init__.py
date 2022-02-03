from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from apifairy import APIFairy

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
apifairy = APIFairy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_object(test_config)

    db.init_app(app)
    migrate.init_app(app, db, directory=app.config['MIGRATION_DIR'])
    ma.init_app(app)
    apifairy.init_app(app)
    login_manager.init_app(app)

    # cli commands
    from rest_app.database import reset_db_command, populate_db_command
    app.cli.add_command(reset_db_command)
    app.cli.add_command(populate_db_command)

    # blueprints
    from rest_app.api import register_api_blueprints
    register_api_blueprints(app)
    # from rest_app.errors.errors_service import errors
    # app.register_blueprint(errors)
    from rest_app.views import register_view_blueprints
    register_view_blueprints(app)

    return app
