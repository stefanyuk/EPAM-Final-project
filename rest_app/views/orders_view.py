from flask import Blueprint, render_template

order = Blueprint('orders', __name__, url_prefix='/order')


@order.route('/<string:user_id>')
def user_orders_list(user_id):
    pass


@order.route('/<string:order_id>')
def order_detail(order_id):
    pass


@order.route('/create')
def create_order():
    pass


@order.route('/<string:order_id>/update')
def update_order(order_id):
    pass


@order.route('/<string:order_id>/delete')
def delete_order(order_id):
    pass