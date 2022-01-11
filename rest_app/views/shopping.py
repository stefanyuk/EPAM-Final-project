from flask import Blueprint, render_template, url_for, request, session, flash, redirect, jsonify
from flask_login import current_user
from rest_app.service.product_service import product_data_to_dict
from rest_app.models import Product

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

    page = request.args.get('page', 1, type=int)
    products_pagination = Product.query.order_by(Product.category_id.asc()).paginate(page=page, per_page=6)
    product_info = [product_data_to_dict(product) for product in products_pagination.items]

    return render_template(
        'products_main.html',
        products=product_info,
        products_pagination=products_pagination
    )


@shopping.route('/add_product', methods=['POST'])
def update_cart():
    if current_user.is_authenticated:
        product_id = request.form['id']

        if not session.get('items_in_cart', None):
            session['items_in_cart'] = []

        if product_id not in session['items_in_cart']:
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
    session.clear()
    return redirect('url_for('')')