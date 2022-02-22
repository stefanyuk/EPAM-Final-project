from flask import request
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


def search_table(model, schema):
    """Runs a server-side filtering, searching and filtering of the specified table"""
    query = model.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = model.table_search(query, search)
    else:
        order = model.sort_by_column()

        if isinstance(order, list):
            query = query.order_by(*order)
        else:
            query = order

    total_filtered = query.count()

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [schema.dump(row) for row in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': model.query.count(),
        'draw': request.args.get('draw', type=int),
    }