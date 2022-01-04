from sqlalchemy import exc
from flask import jsonify
from flask_restful import Resource
from rest_app.service.order_service import *
from rest_app.error_services.error_messages import error_order_not_found
from rest_app.service.common_services import *
from rest_app.rest.auth import auth
# TODO check how to define __all__ in module


class OrdersAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        orders = get_all_rows_from_db(Order)
        orders_list = [order_data_to_dict(order) for order in orders]

        return jsonify(orders_list)

    def post(self):
        args = order_data_parser().parse_args()
        args = {k: args[k] for k in list(args)[1:]}

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
            return error_order_not_found, 404

        return order_data_to_dict(order)

    def put(self, order_id):
        """
        Updates information about the specific order in the database

        :param order_id: id of the order
        """
        args = order_data_parser().parse_args()

        try:
            update_order(order_id, **args)
        except exc.NoResultFound:
            return error_order_not_found, 404

        return {'message': f'order - {order_id} - has been updated'}

    def delete(self, order_id):
        """
        Deletes specified order from the database

        :param order_id: id of the order
        """
        try:
            delete_row_by_id(Order, order_id)
        except exc.NoResultFound:
            return error_order_not_found, 404

        return {'message': f'order - {order_id} - has been deleted'}
