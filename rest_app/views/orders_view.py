from flask import Blueprint, render_template, request
from rest_app.service.order_service import get_all_client_orders, order_data_to_dict
from rest_app.models import Order

order = Blueprint('orders', __name__, url_prefix='/order')


@order.route('/<string:user_id>')
def user_orders_list(user_id):
    page = request.args.get('page', 1, type=int)
    query = get_all_client_orders(user_id)
    orders_pagination = query.paginate(page=page, per_page=3)
    orders_info = [order_data_to_dict(order) for order in orders_pagination.items]

    return render_template('user_orders_main.html', orders=orders_info, orders_pagination=orders_pagination)


@order.route('/detail/<string:order_id>')
def order_detail(order_id):
    order = Order.query.get(order_id)
    order_time = order.order_time.strftime('%H:%M')
    order_date = order.order_date.strftime('%d %B, %Y')

    return render_template('order_details.html', order=order, order_time=order_time, order_date=order_date)


@order.route('/<string:order_id>/delete')
def delete_order(order_id):
    pass