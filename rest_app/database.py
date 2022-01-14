from uuid import uuid4
from flask.cli import with_appcontext
import click
from werkzeug.security import generate_password_hash
from rest_app import db
from rest_app.models import User
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles
from rest_app.populate_db_with_data import main


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


def reset_db():
    db.drop_all()
    db.create_all()
    create_superuser()


@click.command('reset-db')
@with_appcontext
def reset_db_command():
    """Clear the existing data and create new tables."""
    reset_db()
    click.echo('Database has been reset.')


@click.command('populate-db')
@with_appcontext
def populate_db_command():
    main(200)
    click.echo('Test data has been added to the database.')


def create_superuser():
    admin_user_info = {
        'id': str(uuid4()),
        'username': 'admin',
        'password_hash': generate_password_hash('admin'),
        'last_name': 'Admin',
        'is_admin': True,
        'is_employee': True,
        'email': 'admin'
    }

    user = User(**admin_user_info)

    db.session.add(user)
    db.session.commit()
