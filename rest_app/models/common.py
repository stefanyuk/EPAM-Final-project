from rest_app import db


class Common:
    """Model that represents common CRUD operations for all models"""
    def update(self, data):
        """Partially updates requested fields of the specified record"""
        for attr, value in data.items():
            setattr(self, attr, value)

        db.session.commit()

    @classmethod
    def delete(cls, model_id):
        """Deletes specified row"""
        db.session.query(cls).filter(cls.id == model_id).delete()
        db.session.commit()

    @classmethod
    def get_by_name(cls, name):
        """Retrieves row by name attribute"""
        return cls.query.filter_by(name=name).first()

