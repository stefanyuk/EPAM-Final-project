from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import current_user
from rest_app.forms.admin_forms import UpdateOrder
from rest_app.service.order_item_service import create_order_items
from rest_app.service.address_service import address_data_form_parser, add_address, check_if_address_exists
from rest_app.service.order_service import create_order, update_order
from rest_app.models import Order, User

order = Blueprint('orders', __name__, url_prefix='/order')


@order.route('/<string:order_id>/update', methods=['GET', 'POST'])
def order_update(order_id):
    form = UpdateOrder()

    if form.validate_on_submit():
        update_order(order_id, 'id', status=form.status.data)
        flash('Order was successfully updated', 'success')
        return redirect(url_for('admin.admin_main'))

    return render_template('order_update.html', form=form)


@order.route('/<string:user_id>')
def user_orders_list(user_id):
    """
    Selects all orders that were placed by a specified user
    :param user_id: unique id of the user
    """
    page = request.args.get('page', 1, type=int)
    query = User.query.get(user_id).orders
    orders_pagination = query.paginate(page=page, per_page=3)
    orders_info = [order.data_to_dict() for order in orders_pagination.items]

    return render_template('user_orders_main.html', orders=orders_info, orders_pagination=orders_pagination)


@order.route('/detail/<string:order_id>')
def order_detail(order_id):
    """
    Returns information about specified order
    :param order_id: unique id of the order
    """
    order = Order.query.get(order_id)
    order_time = order.order_time.strftime('%H:%M')
    order_date = order.order_date.strftime('%d %B, %Y')

    return render_template('order_details.html', order=order, order_time=order_time, order_date=order_date)


@order.route('/<string:order_id>/delete')
def cancel_order(order_id):
    """Cancels specified order"""
    order = Order.query.get(order_id)

    if order.status == 'awaiting fulfilment':
        update_order(order_id, 'id', status='canceled')
        flash('Order was successfully canceled', 'success')
        if current_user.is_admin:
            return redirect(url_for('admin.admin_main'))
        return redirect(url_for('orders.user_orders_list', user_id=current_user.id))


def finalize_order_creation(address_form):
    """
    Finalizes creation of the order, that was placed by user
    :param address_form: form with address data provided by user
    """
    address = check_if_address_exists(address_form).first()
    if not address:
        args = address_data_form_parser().parse_args()
        address = add_address(user_id=current_user.id, **args)

    new_order = create_order(
        session.get('order_items_info'), user_id=current_user.id, address_id=address.id, main_key='id'
    )
    create_order_items(session.get('order_items_info'), new_order.id, main_key='id')
    flash('Your order was successfully created', 'success')
