from marshmallow import validates, ValidationError, post_load
from rest_app import ma
from rest_app.models import Product, Category


class ProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field(required=True)
    summary = ma.auto_field()
    price = ma.auto_field(required=True)
    category_name = ma.String(required=True, load_only=True)

    @validates('category_name')
    def validate_category_name(self, value):
        """Verifies whether category exists"""
        if not Category.query.filter_by(name=value).first():
            raise ValidationError('Category with the provided name does not exist')

    @validates('title')
    def validate_product_title(self, value):
        """Validates whether product with the provided title does not exist"""
        if Product.query.filter_by(title=value).first():
            raise ValidationError('Product with the provided name already exists')

    @post_load
    def add_product_id(self, data, **kwargs):
        """Adds product id to schema load result"""
        category = Category.query.filter_by(name=data.pop('category_name')).first()
        data['category_id'] = category.id
        return data
