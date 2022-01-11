from flask import Blueprint, render_template, url_for, request, session, flash, redirect, jsonify
from flask_login import current_user
from rest_app.service.product_service import product_data_to_dict
from rest_app.service.common_services import get_all_rows_from_db
from rest_app.models import Product, Category, Address
from rest_app.forms.personal_info_forms import AddressForm, add_values_to_address_form

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


@shopping.route('/products/<string:category_id>')
def products_by_category(category_id):
    categories = [category for category in get_all_rows_from_db(Category)]
    # category = Category.query.filter(Category.name == category_name).one()

    page = request.args.get('page', 1, type=int)
    products_pagination = Product.query.filter(Product.category_id == category_id).paginate(page=page, per_page=6)
    product_info = [product_data_to_dict(product) for product in products_pagination.items]

    return render_template(
        'products_main.html',
        products=product_info,
        products_pagination=products_pagination,
        categories=categories
    )



@shopping.route('/add_product', methods=['POST'])
def update_cart():
    if current_user.is_authenticated:
        product_id = request.form['id']

        if not session.get('items_in_cart', None):
            session['items_in_cart'] = []

        if product_id in session['items_in_cart']:
            flash('Item is already in the cart', 'info')
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


@shopping.route('/delete_item/<string:product_id>')
def delete_item_from_cart(product_id):
    session.get('items_in_cart').remove(product_id)
    session.modified = True


@shopping.route('/finalize_checkout', methods=['GET', 'POST'])
def finalize_checkout():
    form = add_values_to_address_form(AddressForm(), Address, current_user.id)
    form.submit.label.text = 'Get Delivery'

    if len(current_user.addresses.all()) > 1:
        session['add_address_info'] = True

    return render_template('finalize_order.html', address_form=form)

