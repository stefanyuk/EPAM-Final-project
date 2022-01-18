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


def sort_table_by_field(table, field_name, sort_order='asc', table_to_join=None):
    """
    Creates a query to sort the table by provided field name

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


def update_table_row(table_to_update, row_id, **kwargs):
    """
    Partially updates specified table according to provided data

    :param table_to_update: table where is record that needs to be updated
    :param row_id: id of the row to update
    :param kwargs: fields that need to be updated
    """
    table = get_row_by_id(table_to_update, row_id)

    for key, value in kwargs.items():
        if value:
            setattr(table, key, value)

    db.session.commit()

# We use it in order to sort table in a chosen by user order
order = {
    'asc': asc,
    'desc': desc
}