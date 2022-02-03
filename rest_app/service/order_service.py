from sqlalchemy import func, asc, desc
from rest_app import db
from rest_app.models import OrderItem, Product


def get_order_total_value(sort_order='asc'):
    order = asc if sort_order == 'asc' else desc

    query = db.session.query(OrderItem, func.SUM(Product.price * OrderItem.quantity).label('total_price')) \
        .join(Product)\
        .group_by(OrderItem.order_id)\
        .order_by(order('total_price'))

    return query
