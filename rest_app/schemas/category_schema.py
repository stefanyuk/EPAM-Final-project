from marshmallow import validates, ValidationError
from rest_app import ma
from rest_app.models import Category


class CategorySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Category

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    products = ma.List(ma.Pluck('ProductSchema', 'title'), dump_only=True)

    @validates('name')
    def validate_name(self, value):
        """Validates whether category with the provided name already exists"""
        category = Category.query.filter_by(name=value).first()

        if category:
            raise ValidationError('Category with this name already exists')
