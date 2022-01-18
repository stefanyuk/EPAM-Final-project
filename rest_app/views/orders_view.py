from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import current_user
from sqlalchemy import and_
from rest_app.service.order_service import get_all_client_orders, order_data_to_dict
from rest_app.service.common_services import delete_row_by_id
from rest_app.service.order_item_service import create_order_items
from rest_app.service.address_service import address_data_form_parser, add_address
from rest_app.service.order_service import create_order
from rest_app.models import Order, Address

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
    order = Order.query.get(order_id)

    if order.status == 'awaiting fulfilment':
        delete_row_by_id(Order, order_id)
        flash('Order was successfully canceled', 'success')
        if current_user.is_admin:
            return redirect(url_for('admin.admin_main'))
        return redirect(url_for('orders.user_orders_list', user_id=current_user.id))


def finalize_order(address_form):
    address = Address.query.filter(
        and_(
            Address.user_id == current_user.id,
            Address.street == address_form.street.data,
            Address.street_number == str(address_form.street_number.data)
        )
    ).first()
    if not address:
        args = address_data_form_parser().parse_args()
        address = add_address(user_id=current_user.id, **args)

    new_order = create_order(
        session.get('order_items_info'), user_id=current_user.id, address_id=address.id, main_key='id'
    )
    create_order_items(session.get('order_items_info'), new_order.id, main_key='id')
    flash('Your order was successfully created', 'success')
