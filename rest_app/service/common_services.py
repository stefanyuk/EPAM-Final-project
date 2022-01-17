from sqlalchemy import asc, desc
from rest_app import db


def delete_row_by_id(model, model_id):
    """Deletes the table row with the specified id"""

    db.session.query(model).filter(model.id == model_id).delete()
    db.session.commit()


def get_row_by_id(model, model_id):
    """
    This function is used to get the single row from the database by id

    :param model: table where row needs to be find
    :param model_id: unique id of the record in the table
    :return: data from the row with the specified id
    """

    row = db.session.query(model).filter(model.id == model_id).one()

    return row


def get_all_rows_from_db(model):
    """
    Returns all rows from the specified table

    :param model: table where rows needs to be returned
    """
    models = model.query.all()

    return models


def sort_table_by_field(table, field_name, sort_order='asc', table_to_join=None):
    """
    Creates a query to sort the users table by provided field name

    :param table: table that needs to be sorted
    :param table_to_join: table that needs to be joined to perform a search
    :param field_name: name according to which table needs to be sorted
    :param sort_order: order in which table needs to be sorted
    """
    if table_to_join:
        query = table.query.join(table_to_join).order_by(order[sort_order](field_name))
    else:
        query = table.query.order_by(order[sort_order](field_name))

    return query


def set_all_parser_args_to_unrequired(parser):
    """
    Sets all parser arguments to unrequired

    :param parser: parser that needs to be reset
    """
    for arg in parser.args:
        if arg.required:
            arg.required = False

    return parser

# We use it in order to sort table in a chosen by user order
order = {
    'asc': asc,
    'desc': desc
}