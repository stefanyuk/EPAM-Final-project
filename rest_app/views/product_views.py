from flask import Blueprint, render_template, flash, redirect, url_for
from rest_app.forms.admin_forms import AddProduct
from rest_app.service.product_service import add_product, product_form_data_parser
from rest_app.models import Category

product = Blueprint('product', __name__, url_prefix='/product')


@product.route('/create', methods=['GET', 'POST'])
def product_add():
    form = AddProduct()
    form.populate_choices_fields()

    if form.validate_on_submit():
        args = product_form_data_parser().parse_args()
        category = Category.query.filter_by(name=args['category']).first()
        args.pop('category')
        add_product(category_id=category.id, **args)
        flash('Product was added to the database', 'success')
        return redirect(url_for('admin.admin_main'))

    return render_template('add_product.html', form=form)
