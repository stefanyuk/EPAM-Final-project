from marshmallow import validates, ValidationError, validates_schema
from sqlalchemy import and_
from rest_app import ma
from rest_app.models import Address, User


class AddressSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Address

    id = ma.auto_field(dump_only=True)
    user = ma.Pluck('UserSchema', 'username', dump_only=True)
    user_id = ma.auto_field(required=True, error_messages={"required": "User id is required."}, load_only=True)
    city = ma.auto_field(required=True)
    street = ma.auto_field(required=True)
    street_number = ma.auto_field(required=True)
    postal_code = ma.auto_field(required=True)

    @validates('street_number')
    def validate_street_number(self, value):
        """Validates whether street number is a digit"""
        if not isinstance(value, int):
            raise ValidationError('Street number must be a digit')

    @validates('user_id')
    def validate_user_id(self, value):
        """Validates user id"""
        if not User.query.get(value):
            raise ValidationError('User with the provided id does not exist')

    @validates_schema(skip_on_field_errors=True)
    def validate_schema(self, data, **kwargs):
        """
        Verifies whether address already exists in the list
        of addresses of the specified user
        """
        query = Address.query.filter(
            and_(
                Address.user_id == data.get('user_id'),
                Address.city == data.get('city'),
                Address.street == data.get('street'),
                Address.street_number == data.get('street_number')
            )
        )

        if query.first():
            raise ValidationError('This address already exists in the list of addresses of the specified user')


