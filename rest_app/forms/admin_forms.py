from datetime import datetime
from flask_wtf import FlaskForm
import phonenumbers
from wtforms import TextAreaField, SubmitField, ValidationError, StringField, BooleanField, SelectField, \
    FloatField, DateField, IntegerField, PasswordField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Optional, Length
from rest_app.models import Department, Category, Product, EmployeeInfo
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
            dept = Department.query.filter_by(name=name.data).first()
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
    def __init__(self, employee_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.employee_id = employee_id

    def prepopulate_values(self):
        employee = EmployeeInfo.query.filter_by(id=self.employee_id).first()

        self.first_name.data = employee.user.first_name
        self.last_name.data = employee.user.last_name
        self.department.data = employee.department.name
        self.salary.data = employee.salary
        self.hire_date.data = employee.hire_date
        self.submit.label.text = 'Update'


class UpdateOrder(FlaskForm):
    status = SelectField('Status', choices=['delivered', 'awaiting fulfilment', 'canceled'])

    submit = SubmitField('Update')


class AddUser(UserForm, FlaskForm):
    phone_number = StringField('Phone Number', validators=[Optional()])
    is_admin = BooleanField('Is admin?')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=30)])
    submit = SubmitField('Create')

    def validate_phone_number(self, phone_number):
        try:
            p = phonenumbers.parse(phone_number.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')


class AddProduct(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('Summary', validators=[Optional()])
    price = FloatField('Price', validators=[DataRequired()])
    category_name = SelectField('Category', choices=[], validators=[DataRequired()])
    image_file = FileField('Update product picture', validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
    submit = SubmitField('Create')

    def validate_title(self, title):
        """Validates whether product with the provided title does not exist"""
        if Product.query.filter_by(title=title.data).first():
            raise ValidationError('Product with this name already exists')

    def populate_choices_fields(self):
        """Adds categories to choices field"""
        self.category_name.choices = [category.name for category in Category.query.all()]


class UpdateProduct(AddProduct, FlaskForm):
    def __init__(self, product_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_id = product_id

    def validate_title(self, title):
        """Validates whether product with the provided title does not exist"""
        product = Product.query.filter_by(id=self.product_id).first()
        if title.data != product.title:
            product = Product.query.filter_by(title=title.data).first()
            if product:
                raise ValidationError('Product with this name already exists')

    def prepopulate_values(self):
        product = Product.query.filter_by(id=self.product_id).first()

        self.title.data = product.title
        self.summary.data = product.summary
        self.price.data = product.price
        self.category_name.choices = [product.category.name] + [category.name for category in Category.query.all() if category.name != product.category.name]
        self.submit.label.text = 'Update'
