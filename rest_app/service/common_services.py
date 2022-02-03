from sqlalchemy import asc, desc


def sort_table_by_field(table, field_name, sort_order='asc', table_to_join=None):
    """
    Creates a query to sort the table by provided field name

    :param table: table that needs to be sorted
    :param table_to_join: table that needs to be joined to perform a search
    :param field_name: name according to which table needs to be sorted
    :param sort_order: order in which table needs to be sorted
    """
    order = asc if sort_order == 'asc' else desc

    if table_to_join:
        query = table.query.join(table_to_join).order_by(order(field_name))
    else:
        query = table.query.order_by(order(field_name))

    return query
