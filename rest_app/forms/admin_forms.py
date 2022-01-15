from flask_wtf import FlaskForm
from wtforms.widgets import TelInput
import phonenumbers
from wtforms import TextAreaField, SubmitField, ValidationError, StringField, BooleanField, SelectField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Optional
from rest_app.models import Department, User, Category, Product, EmployeeInfo


class AddDepartment(FlaskForm):
    name = StringField('Department Name', validators=[DataRequired()])
    description = TextAreaField('Description')

    def validate_name(self, name):
        dept = Department.query.filter(Department.name == name).first()

        if dept:
            raise ValidationError('Department with this name already exists')


class AddEmployee(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    department = SelectField(
        'Department',
        choices=['1', '2', '3'],
        validators=[DataRequired()]
    )
    salary = FloatField('Salary', validators=[DataRequired()])
    submit = SubmitField('Add')


class AddUser(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=30)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone_number = IntegerField('Phone Number', widget=TelInput())
    is_employee = BooleanField('Is employee?')
    is_admin = BooleanField('Is admin?')
    submit = SubmitField('Add')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter(User.email == email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_phone_number(self, phone_number):
        start = phone_number.data[:2]
        if start != '+1':
            raise ValidationError('Number should start with +1')
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


class FilterUserForm(FilterForm, FlaskForm):
    is_employee = SelectField('Is Employee', choices=[True, False], validators=[Optional()])

    def populate_choices_fields(self):
        main_fields = ['username', 'last_name', 'first_name', 'last_login_date', 'total_money_spent']

        for row_title in main_fields:
            self.field_name.choices.append(row_title)
