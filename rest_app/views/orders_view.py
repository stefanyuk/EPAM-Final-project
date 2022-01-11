from flask import Blueprint, render_template

order = Blueprint('order', __name__, url_prefix='/order')


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