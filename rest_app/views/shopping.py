from flask import Blueprint, render_template, url_for, request, session, flash, redirect, jsonify
from flask_login import current_user
from sqlalchemy import and_
from rest_app.service.product_service import product_data_to_dict
from rest_app.service.address_service import address_data_to_dict
from rest_app.service.order_service import create_order
from rest_app.service.address_service import add_address
from rest_app.service.order_item_service import create_order_items
from rest_app.service.common_services import get_all_rows_from_db
from rest_app.models import Product, Category, Address, Order
from rest_app.forms.personal_info_forms import AddressForm

shopping = Blueprint('shop', __name__)


@shopping.route('/')
def welcome_landing():
    login_url = url_for('auth.login')
    log_out_url = url_for('auth.logout')
    register_url = url_for('auth.register')

    return render_template(
        'welcome_landing.html',
        login_url=login_url,
        log_out_url=log_out_url,
        register_url=register_url
    )



@shopping.route('/products')
def products():
    categories = [category for category in get_all_rows_from_db(Category)]

    page = request.args.get('page', 1, type=int)
    products_pagination = Product.query.order_by(Product.category_id.asc()).paginate(page=page, per_page=6)
    product_info = [product_data_to_dict(product) for product in products_pagination.items]

    return render_template(
        'products_main.html',
        products=product_info,
        products_pagination=products_pagination,
        categories=categories
    )


@shopping.route('/products/<string:category_name>')
def products_by_category(category_name):
    categories = [category for category in get_all_rows_from_db(Category)]
    category = Category.query.filter(Category.name == category_name).one()

    page = request.args.get('page', 1, type=int)
    products_pagination = Product.query.filter(Product.category_id == category.id).paginate(page=page, per_page=6)
    product_info = [product_data_to_dict(product) for product in products_pagination.items]

    return render_template(
        'products_main.html',
        products=product_info,
        products_pagination=products_pagination,
        categories=categories
    )


@shopping.route('/add_item_to_cart', methods=['POST'])
def add_item_to_cart():
    if current_user.is_authenticated:
        product_id = request.form['id']

        if not session.get('items_in_cart', None):
            session['items_in_cart'] = []

        if product_id in session['items_in_cart']:
            return jsonify({'message': 'item is already in the cart'})
        else:
            session['items_in_cart'].append(
                product_id
            )
            session.modified = True

        return render_template('add_to_cart_update.html')
    else:
        flash('Please log in in order to add items to the cart', 'info')
        return jsonify({'url': url_for('auth.login')})


@shopping.route('/checkout')
def checkout():
    cart_items = []

    for cart_item in session.get('items_in_cart'):
        product = Product.query.get(cart_item)
        cart_items.append(
            product_data_to_dict(product)
        )

    return render_template('checkout.html', cart_items=cart_items, hide_checkout=True)


@shopping.route('/empty_cart')
def empty_cart():
    session.get('items_in_cart').clear()
    session.modified = True
    return redirect(url_for('shop.products'))


@shopping.route('/delete_item/<string:product_id>', methods=['POST'])
def delete_item_from_cart(product_id):
    session.get('items_in_cart').remove(product_id)
    session.modified = True

    if not session.get('items_in_cart'):
        return jsonify({'url': url_for('shop.products')})

    return render_template('add_to_cart_update.html')


@shopping.route('/finalize_order', methods=['GET', 'POST'])
def finalize_checkout():
    address_form = AddressForm()

    if address_form.validate_on_submit():
        address = Address.query.filter_by(and_(
            user_id=current_user.id,
            street_name=address_form.data['street_name'],
            street_number=address_form.data['street_number']
        )).first()
        if not address:
            pass
        create_order(
            session.get('order_items_info'),
            user_id=current_user.id,

        )



    addresses = Address.query.filter(Address.user_id == current_user.id).all()
    if addresses:
        address_form.change_address_values(addresses.pop())

    address_form.submit_address.label.text = 'Get Delivery'

    return render_template('finalize_order.html', address_form=address_form)


@shopping.route('/get_storage_values', methods=['POST'])
def get_values_from_local_storage():
    session['order_items_info'] = request.get_json()['order_items_info']
    session.modified = True

    return '', 204


@shopping.route('/update_address_values/<string:address_id>', methods=['POST'])
def get_address_values(address_id):
    address = Address.query.get(address_id)
    address_info = address_data_to_dict(address)

    return jsonify(address_info)
