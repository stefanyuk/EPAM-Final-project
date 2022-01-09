from flask_restful import reqparse
from rest_app.models import Vacation
from uuid import uuid4
from rest_app import db
from rest_app.service.common_services import get_row_by_id


def add_vacation(employee_id, vacation_start, vacation_end):
    vacation = Vacation(
        id=str(uuid4()),
        employee_id=employee_id,
        vacation_start=vacation_start,
        vacation_end=vacation_end
    )

    db.session.add(vacation)
    db.session.commit()

    return vacation


def vacation_data_to_dict(vacation):
    vacation_info = {
        'employee_id': vacation.employee_id,
        'first_name': vacation.employee.user.first_name,
        'last_name': vacation.employee.user.last_name,
        'vacation_start': vacation.vacation_start,
        'vacation_end': vacation.vacation_end
    }

    return vacation_info


def vacation_data_parser():
    """
    Creates a parser in order to parse information about vacation
    provided by user
    """
    parser = reqparse.RequestParser()

    parser.add_argument('employee_id', type=str, help='you did not provide employee id', required=True)
    parser.add_argument('vacation_start', type=str, help='you did not provide vacation start', required=True)
    parser.add_argument('vacation_end', type=str, help='you did not provide vacation end', required=True)


def update_vacation(vacation_id, **kwargs):
    vacation = get_row_by_id(Vacation, vacation_id)

    for field in kwargs:
        if kwargs[field]:
            setattr(vacation, field, kwargs[field])

    db.session.commit()