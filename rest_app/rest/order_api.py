from sqlalchemy import exc
from flask import jsonify
from flask_restful import Resource
from rest_app.service.order_service import *
from rest_app.errors.error_messages import record_not_found_by_id_error
from rest_app.service.common_services import *
from rest_app.rest.auth import auth
# TODO check how to define __all__ in module


class OrdersAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        orders = get_all_rows_from_db(Order)
        orders_list = [order_data_to_dict(order) for order in orders]

        return orders_list

    def post(self):
        args = create_order_data_parser().parse_args()
        order_id = create_order(**args)

        return {'message': f'Order with the number {order_id} has been created'}, 201


class OrderAPI(Resource):
    """
    Resource that handles HTTP requests related to the specific order in the database
    """
    decorators = [auth.login_required]

    def get(self, order_id):
        """
        Returns order with the specified id

        :param order_id: id of the order
        """
        try:
            order = get_row_by_id(Order, order_id)
        except exc.NoResultFound:
            return record_not_found_by_id_error('order'), 404

        return order_data_to_dict(order)

    def put(self, order_id):
        """
        Updates information about the specific order in the database

        :param order_id: id of the order
        """
        args = update_order_data_parser().parse_args()

        try:
            update_order(order_id, **args)
        except exc.NoResultFound:
            return record_not_found_by_id_error('order'), 404

        return {'message': f'order - {order_id} - has been updated'}

    def delete(self, order_id):
        """
        Deletes specified order from the database

        :param order_id: id of the order
        """
        delete_row_by_id(Order, order_id)

        return '', 204
