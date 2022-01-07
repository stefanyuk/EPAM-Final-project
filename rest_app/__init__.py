from flask import Flask
from config import DevelopmentConfig, Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(test_config)

    db.init_app(app)
    migrate.init_app(app, db, directory=app.config['MIGRATION_DIR'])

    from rest_app.database import reset_db_command
    app.cli.add_command(reset_db_command)

    from rest_app.rest import rp_api
    app.register_blueprint(rp_api)
    from rest_app.errors.errors_service import errors
    app.register_blueprint(errors)
    from rest_app.views.welcome import wlc
    app.register_blueprint(wlc)

    # @app.route('/')
    # def index():
    #     return {
    #         'api_version': 1,
    #         'correct_url': f'/api/v{Config.API_VERSION}/...'
    #     }

    return app
