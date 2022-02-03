from apifairy import body, response, other_responses
from flask import Blueprint
from rest_app import db
from rest_app.models import Product
from rest_app.schemas import ProductSchema

products = Blueprint('products', __name__, url_prefix='/api/v1')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@products.route('/products', methods=['GET'])
@response(products_schema)
def get_all():
    """Retrieve all products"""
    return Product.query.all()


@products.route('/products', methods=['POST'])
@body(product_schema)
@response(product_schema)
def new(args):
    """Create new product"""
    product = Product.create(**args)
    db.session.add(product)
    db.session.commit()

    return product


@products.route('/products/<uuid:product_id>', methods=['GET'])
@response(product_schema)
@other_responses({404: 'Product not found'})
def get(product_id):
    """Retrieve a product by id"""
    return Product.query.get_or_404(product_id)


@products.route('/products/<string:name>', methods=['GET'])
@response(product_schema)
@other_responses({404: 'Product not found'})
def get_by_name(name):
    """Retrieve a product by name"""
    return Product.query.filter_by(name=name).first_or_404()


@products.route('/products/<string:product_id>', methods=['PATCH'])
@body(product_schema)
@response(product_schema)
def update(args, product_id):
    """Update product information"""
    product = Product.query.get_or_404(product_id)
    product.update(args)
    return product


@products.route('/products/<string:product_id>', methods=['DELETE'])
@other_responses({204: 'No content'})
def delete(product_id):
    """Delete user"""
    Product.query.get(product_id).delete()
    db.session.commit()
    return '', 204
