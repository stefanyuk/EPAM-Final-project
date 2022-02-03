from sqlalchemy import and_
from flask_login import current_user
from rest_app.models import Address


def check_if_address_exists(address_form):
    """
    Verifies whether address already exists in the list
    of addresses of the specified user
    """
    query = Address.query.filter(
        and_(
            Address.user_id == current_user.id,
            Address.street == address_form.street.data,
            Address.street_number == str(address_form.street_number.data)
        )
    )

    return query
