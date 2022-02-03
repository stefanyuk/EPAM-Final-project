from flask import Blueprint, render_template, flash, redirect, url_for
from marshmallow import EXCLUDE
from rest_app.forms.admin_forms import AddProduct
from rest_app.schemas import ProductSchema
from rest_app.models import Product

product = Blueprint('product', __name__, url_prefix='/product')
product_schema = ProductSchema(unknown=EXCLUDE)


@product.route('/create', methods=['GET', 'POST'])
def product_create():
    """Creates new product"""
    form = AddProduct()
    form.populate_choices_fields()

    if form.validate_on_submit():
        data = product_schema.load(form.data)
        Product.create(**data)
        flash('Product was added to the database', 'success')
        return redirect(url_for('admin.admin_main'))

    return render_template('add_product.html', form=form)
