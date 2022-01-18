from sqlalchemy import exc
from flask import jsonify
from flask_restful import Resource
from rest_app.service.product_service import *
from rest_app.service.common_services import *
from rest_app.errors.error_messages import record_not_found_by_id_error
from rest_app.rest.auth import auth
from rest_app.models import Product


class ProductsAPI(Resource):
    """
    Resource that handles HTTP requests related to all products registered in the database
    """
    decorators = [auth.login_required]

    def get(self):
        """
        Returns list of all products
        """
        products = Product.query.all()
        products_list = [product.data_to_dict() for product in products]

        return jsonify(products_list)

    def post(self):
        """
        Creates a new product record in the database
        """
        args = product_data_parser().parse_args()
        product_id = add_product(**args)

        return {'message': f'product with id - {product_id} - has been created'}, 201


class ProductAPI(Resource):
    """
    Resource that handles HTTP requests related to the specific products in the database
    """
    decorators = [auth.login_required]

    def get(self, product_id):
        """
        Returns product with the specified id

        :param product_id: unique id that identifies product
        """
        try:
            product = get_row_by_id(Product, product_id)
        except exc.NoResultFound:
            return record_not_found_by_id_error('product'), 404

        return product.data_to_dict()

    def patch(self, product_id):
        """
        Updates information about the specific product in the database

        :param product_id: unique id that identifies product
        """
        args = product_update_data_parser().parse_args()

        try:
            update_table_row(Product, product_id, **args)
        except exc.NoResultFound:
            return record_not_found_by_id_error('product'), 404

        return {'message': f'product - {product_id} - has been updated'}

    def delete(self, product_id):
        """
        Deletes specified product from the database

        :param product_id: unique id that identifies product
        """
        delete_row_by_id(Product, product_id)

        return '', 204
