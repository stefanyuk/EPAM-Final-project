import secrets
import os
from uuid import uuid4
from sqlalchemy import or_
from flask import current_app
from rest_app import db
from rest_app.models import Category
from rest_app.models.common import Common


class ProductSearch():

    @staticmethod
    def verify_colum_name(col_name):
        if col_name not in ['category', 'title', 'price']:
            col_name = 'title'

        return col_name

    @classmethod
    def sort_by_category(cls, order):
        """
        Creates a query that sorts a category column
        of the Product table in a specified order
        """
        query = db.session.query(Product.id, Product.title, Product.price, Category.name) \
            .join(Category) \
            .order_by(order(Category.name))

        return query

    @classmethod
    def table_search(cls, query, search):
        """Performs a search on the specific fields of the Product table according to the provided data"""

        query = db.session.query(Product.id, Product.title, Product.price, Category.name) \
            .join(Category) \
            .filter(
            or_(
                Product.title.like(f'%{search}%'),
                Category.name.like(f'%{search}%')
            )
        )

        return query


class Product(Common, ProductSearch, db.Model):
    __tablename__ = 'product'

    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    summary = db.Column(db.Text)
    price = db.Column(db.Numeric(7, 2), nullable=False)
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    category_id = db.Column(db.ForeignKey('category.id', ondelete='SET NULL'), nullable=False)
    image_file = db.Column(db.String, nullable=False, default='black@4x.png')

    @classmethod
    def create(cls, **kwargs):
        """Creates new product"""
        product = cls(id=str(uuid4()), **kwargs)
        db.session.add(product)
        db.session.commit()
        return product

    @property
    def category_name(self):
        return self.category

    def save_product_picture(self, form_picture):
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(current_app.root_path, 'static/img/product_pics')
        os.remove(os.path.join(picture_path, self.image_file))
        form_picture.save(os.path.join(picture_path, picture_fn))
        self.image_file = picture_fn
        db.session.commit()

        return picture_fn


    @category_name.setter
    def category_name(self, new_category):
        category = Category.query.filter_by(name=new_category).first()
        self.category_id = category.id

    def __repr__(self):
        return f'<Product {self.title}>'
