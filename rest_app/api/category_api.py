from apifairy import body, response, other_responses
from flask import Blueprint
from rest_app import db
from rest_app.models import Category
from rest_app.schemas import CategorySchema, ProductSchema

categories = Blueprint('categories', __name__, url_prefix='/api/v1')

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


@categories.route('/categories', methods=['GET'])
@response(categories_schema)
def get_all():
    """Retrieve all categories"""
    return Category.query.all()


@categories.route('/categories', methods=['POST'])
@body(category_schema)
@response(category_schema)
def new(args):
    """Create new category"""
    return Category.create(**args)


@categories.route('/categories/<uuid:category_id>', methods=['GET'])
@response(category_schema)
@other_responses({404: 'Category not found'})
def get(category_id):
    """Retrieve category by id"""
    return Category.query.get_or_404(str(category_id))


@categories.route('/categories/<string:category_name>', methods=['GET'])
@response(category_schema)
@other_responses({404: 'Category not found'})
def get_by_name(category_name):
    """Retrieve category by name"""
    return Category.query.filter_by(name=category_name).first_or_404()


@categories.route('/categories/<string:category_name>/products', methods=['GET'])
@response(ProductSchema(many=True))
@other_responses({404: 'Category not found'})
def get_category_products(category_name):
    """Retrieve all products of the specified category"""
    category = Category.query.filter_by(name=category_name).first_or_404()
    return category.products


@categories.route('/categories/<string:category_id>', methods=['PATCH'])
@body(category_schema)
@response(category_schema)
def update(args, category_id):
    """Update category information"""
    category = Category.query.get_or_404(category_id)
    category.update(args)
    db.session.commit()
    return category


@categories.route('/categories/<string:category_id>', methods=['DELETE'])
@other_responses({204: 'No content'})
def delete(category_id):
    """Delete category"""
    db.session.query(Category).filter_by(id=category_id).delete()
    db.session.commit()
    return '', 204
