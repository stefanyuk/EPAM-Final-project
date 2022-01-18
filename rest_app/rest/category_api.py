from sqlalchemy import exc
from flask import jsonify
from flask_restful import Resource
from rest_app.service.category_service import *
from rest_app.service.common_services import *
from rest_app.errors.error_messages import record_not_found_by_id_error
from rest_app.rest.auth import auth
from rest_app.models import Category


class CategoriesAPI(Resource):
    """
    Resource that handles HTTP requests related to all categories registered in the database
    """
    decorators = [auth.login_required]

    def get(self):
        """
        Returns list of all categories
        """
        categories = Category.query.all()
        category_list = [category.data_to_dict() for category in categories]

        return jsonify(category_list)

    def post(self):
        """
        Creates a new category record in the database
        """
        args = category_data_parser().parse_args()
        category = add_category(**args)

        return {'message': f'category with id - {category.id} - has been created'}, 201


class CategoryAPI(Resource):
    """
    Resource that handles HTTP requests related to the specific category in the database
    """
    decorators = [auth.login_required]

    def get(self, category_id):
        """
        Returns category with the specified id

        :param category_id: unique id that identifies category
        """
        try:
            category = get_row_by_id(Category, category_id)
        except exc.NoResultFound:
            return record_not_found_by_id_error('product'), 404

        return category.data_to_dict()

    def patch(self, category_id):
        """
        Updates information about the specific category in the database

        :param category_id: unique id that identifies category
        """
        args = category_data_parser().parse_args()

        try:
            update_table_row(category_id, **args)
        except exc.NoResultFound:
            return record_not_found_by_id_error('product'), 404

        return {'message': f'category - {category_id} - has been updated'}

    def delete(self, category_id):
        """
        Deletes specified category from the database

        :param category_id: unique id that identifies category
        """
        delete_row_by_id(Category, category_id)

        return '', 204
