from flask import request

from rest_app import db


class Common:
    """Model that represents common CRUD operations for all models"""

    @classmethod
    def update(cls, model_id, data):
        """
        Partially updates requested fields of the specified record

        :param model_id: id of the table row that needs to be deleted
        :param data: new data
        :return:
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
        order = []
        i = 0
        while True:
            col_index = request.args.get(f'order[{i}][column]')
            if col_index is None:
                break
            col_name = cls.verify_colum_name(request.args.get(f'columns[{col_index}][data]'))
            descending = request.args.get(f'order[{i}][dir]') == 'desc'
            col = getattr(cls, col_name)
            if descending:
                col = col.desc()
            order.append(col)
            i += 1

        return order