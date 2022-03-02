from flask import Blueprint, render_template, flash, redirect, url_for
from marshmallow import EXCLUDE
from rest_app.forms.admin_forms import AddProduct, UpdateProduct
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


@product.route('/<string:product_id>/update', methods=['GET', 'POST'])
def product_update(product_id):
    """Updates specified product"""
    form = UpdateProduct(product_id)
    form.populate_choices_fields()

    if form.validate_on_submit():
        product = Product.query.get(product_id)
        if form.image_file.data:
            product_pic = product.save_product_picture(form.image_file.data)
            form.image_file.data = product_pic
        Product.update(product_id, form.data)
        flash('Product was successfully updated', 'success')
        return redirect(url_for('admin.admin_main'))

    form.prepopulate_values()

    return render_template('add_product.html', form=form, del_btn=True, update=True, product_id=product_id)



@product.route('/<string:product_id>/delete')
def delete_product(product_id):
    """Deletes specified department"""
    Product.delete(product_id)
    flash('Product was successfully deleted', 'success')
    return redirect(url_for('admin.admin_main'))
