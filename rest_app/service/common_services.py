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
