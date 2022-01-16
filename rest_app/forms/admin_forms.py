from datetime import datetime
from flask_wtf import FlaskForm
import phonenumbers
from wtforms import TextAreaField, SubmitField, ValidationError, StringField, BooleanField, SelectField, \
    FloatField, DateField, IntegerField
from wtforms.validators import DataRequired, Optional
from rest_app import db
from rest_app.models import Department, Category, Product, EmployeeInfo, Order, User
from rest_app.forms.auth_forms import UserForm


class AddDepartment(FlaskForm):
    name = StringField('Department Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Create')

    def validate_name(self, name):
        dept = Department.query.filter(Department.name == name.data).first()

        if dept:
            raise ValidationError('Department with this name already exists')


class UpdateDepartment(AddDepartment, FlaskForm):
    def __init__(self, department_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.department_id = department_id

    def validate_name(self, name):
        dept = Department.query.filter_by(id=self.department_id).first()
        if dept.name != name.data:
            dept = Department.query.filter_by(name == name.data).first()
            if dept:
                raise ValidationError('Department with this name already exists')

    def prepopulate_values(self):
        dept = Department.query.filter_by(id=self.department_id).first()
        self.name.data = dept.name
        self.description.data = dept.description
        self.submit.label.text = 'Update'


class AddEmployee(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    department = SelectField('Department', choices=[], validators=[DataRequired()])
    salary = FloatField('Salary', validators=[DataRequired()])
    hire_date = DateField('Hire Date', validators=[Optional()], default=datetime.today)
    available_holidays = IntegerField('Holidays', validators=[Optional()], default=25)
    submit = SubmitField('Create')


class UpdateEmployee(AddEmployee, FlaskForm):
    def __init__(self, employee_id):
        super().__init__()
        self.employee_id = employee_id

    def prepopulate_values(self):
        employee = EmployeeInfo.query.filter_by(id=self.employee_id).first()

        self.first_name.data = employee.user.first_name
        self.last_name.data = employee.user.last_name
        self.department.data = employee.department.name
        self.salary.data = employee.salary
        self.hire_date.data = employee.hire_date
        self.submit.label.text = 'Update'




class AddUser(UserForm, FlaskForm):
    phone_number = StringField('Phone Number', validators=[Optional()])
    is_admin = BooleanField('Is admin?')
    submit = SubmitField('Create')

    def validate_phone_number(self, phone_number):
        try:
            p = phonenumbers.parse(phone_number.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')


class FilterForm(FlaskForm):
    filter_option = SelectField('Filter Options', choices=['', 'Search by', 'Sort By'], validators=[DataRequired()])
    order = SelectField('Sort order', choices=['asc', 'desc'], validators=[Optional()])
    field_name = SelectField('Field Name', choices=[], validators=[Optional()])
    submit = SubmitField('Search')


class FilterProductsForm(FilterForm, FlaskForm):
    category = SelectField('Category', choices=[], validators=[Optional()])

    def populate_choices_fields(self):
        self.category.choices = [category.name for category in Category.query.all()]
        for row_title in Product.__table__.columns.keys():
            if row_title not in ['id', 'order_items', 'category_id', 'summary']:
                self.field_name.choices.append(row_title)


class FilterEmployeesForm(FilterForm, FlaskForm):
    department = SelectField('Department', choices=[], validators=[Optional()])

    def populate_choices_fields(self):
        self.department.choices = [department.name for department in Department.query.all()]

        for row_title in EmployeeInfo.__table__.columns.keys():
            if row_title not in ['id', 'user_id', 'vacations', 'department_id']:
                self.field_name.choices.append(row_title)

        self.field_name.choices += ['last_name', 'first_name']


class FilterUsersForm(FilterForm, FlaskForm):
    is_employee = SelectField('Is Employee', choices=[True, False], validators=[Optional()])

    def populate_choices_fields(self):
        main_fields = ['username', 'last_name', 'first_name', 'last_login_date', 'total_money_spent']

        for row_title in main_fields:
            self.field_name.choices.append(row_title)


class FilterOrdersForm(FilterForm, FlaskForm):
    status = SelectField('Status', choices=[], validators=[Optional()])

    def populate_choices_fields(self):
        statuses = ['delivered', 'awaiting fulfilment', 'canceled']

        for row_title in Order.__table__.columns.keys():
            if row_title not in ['id', 'user_id', 'address_id', 'order_items', 'comments', 'status']:
                self.field_name.choices.append(row_title)

        self.status.choices += statuses


class FilterDepartmentsForm(FilterForm, FlaskForm):
    department = SelectField('Department', choices=[], validators=[Optional()])

    def populate_choices_fields(self):
        self.department.choices = [department.name for department in Department.query.all()]
        self.field_name.choices = ['avg_salary', 'total_employees', 'name']
