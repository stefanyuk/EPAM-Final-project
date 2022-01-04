import json
import random
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from rest_app.models import *


# C:/Users/stefa/Downloads/user.sql
# C:/Users/stefa/Downloads/department.sql
# C:/Users/stefa/Downloads/product.sql
# /home/stefanyuk/database_sqls/user.sql
# /home/stefanyuk/database_sqls/department.sql
# /home/stefanyuk/database_sqls/product.sql

engine = create_engine('postgresql+psycopg2://test:test@localhost:5432/restwebapp')
session = sessionmaker(engine)()


with open(r"C:\Users\stefa\Downloads\employee.json") as f:
    employees = json.load(f)


dept_id = [dept.id for dept in session.query(Department).all()]
user_id = (user.id for user in session.query(User).all())


for employee in employees:
    emp = EmployeeInfo(
        department_id=random.choice(dept_id),
        user_id=next(user_id),
        **employee
    )
    session.add(emp)
    session.commit()


# # query = session.query(Department.dept_name, func.ROUND(func.AVG(EmployeeInfo.salary), 3).label('avg_salary'))\
# #         .join(EmployeeInfo)\
# #         .filter(Department.dept_name == 'Services')\
# #         .group_by(Department.dept_name).one()
# #
# #
# # print(query['avg_salary'])
#
# department = session.query(Department).filter(Department.dept_name == 'asdasdasd').one()
#
#
# print(type(department))




