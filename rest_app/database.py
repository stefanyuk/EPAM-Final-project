from flask.cli import with_appcontext
import click
from rest_app import db
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


def reset_db():
    db.drop_all()
    db.create_all()


@click.command('reset-db')
@with_appcontext
def reset_db_command():
    """Clear the existing data and create new tables."""
    reset_db()
    click.echo('Database has been reset.')


@click.command('db-populate')
@with_appcontext
def populate_db_with_data():
    pass