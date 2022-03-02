from flask import request
from sqlalchemy import asc, desc
from rest_app import db


class Common:
    """Model that represents common operations for all models"""

    @classmethod
    def check_if_regular_col_name(cls, col_name):
        not_regular_col_names = {
            'total_value': 'sort_by_total_value',
            'total_employees': 'sort_by_total_employees',
            'average_salary': 'sort_by_average_salary',
            'first_name': 'sort_by_first_name',
            'last_name': 'sort_by_last_name',
            'total_price': 'sort_by_total_price',
            'category': 'sort_by_category'
        }

        if col_name in ['first_name', 'last_name'] and cls.__name__ != 'EmployeeInfo':
            return None
        return not_regular_col_names.get(col_name)

    @classmethod
    def update(cls, model_id, data: dict):
        """
        Partially updates requested fields of the specified record

        :param model_id: id of the table row that needs to be updated
        :param data: dictionary containing new information about order
        """
        model = cls.query.get(model_id)

        for attr, value in data.items():
            setattr(model, attr, value)

        db.session.commit()
        return model

    @classmethod
    def delete(cls, model_id):
        """
        Deletes specified row
        :param model_id: id of the table row that needs to be deleted
        """
        db.session.query(cls).filter(cls.id == model_id).delete()
        db.session.commit()

    @classmethod
    def get_by_name(cls, name):
        """Retrieves row by name attribute"""
        return cls.query.filter_by(name=name).first()

    @classmethod
    def sort_by_column(cls):
        cols_to_order = []
        i = 0
        while True:
            col_index = request.args.get(f'order[{i}][column]')
            if col_index is None:
                break
            col_name = cls.verify_colum_name(request.args.get(f'columns[{col_index}][data]'))
            order = desc if request.args.get(f'order[{i}][dir]') == 'desc' else asc
            if attr_name := cls.check_if_regular_col_name(col_name):
                return getattr(cls, attr_name)(order)
            descending = request.args.get(f'order[{i}][dir]') == 'desc'
            col = getattr(cls, col_name)
            if descending:
                col = col.desc()
            cols_to_order.append(col)
            i += 1

        return cols_to_order
