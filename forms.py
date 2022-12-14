from ast import ClassDef
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.fields.html5 import DateField

class StudentForm(FlaskForm):
    personal_id_number = StringField("Personal ID Number", validators=[DataRequired(), Length(11,11, message="Personal ID Number has 11 digits")])
    first_name = StringField("First Name", validators=[DataRequired()])
    second_name = StringField("Second Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    field_of_study = SelectField("Field of Study", validators=[DataRequired()], render_kw={"placeholder": "Select"})
    form_of_study = SelectField("Form of Study", validators=[DataRequired()], choices=["full-time", "part-time"], render_kw={"placeholder": "Select"})
    submit = SubmitField("Submit")
    
class FieldForm(FlaskForm):
    field = StringField("Field", validators=[DataRequired()])
    form = SelectField("Form", validators=[DataRequired()])
    capacity = IntegerField("Capacity", validators=[DataRequired()])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    name = StringField("First Name", validators=[DataRequired()])
    surname = StringField("Last Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_repeat = PasswordField("Repeat Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class ApplicationForm(FlaskForm):
    first_name = StringField("First Name",validators=[DataRequired()], render_kw={"placeholder": "First Name"})
    second_name = StringField("Second Name", render_kw={"placeholder": "Second Name (optional)"})
    last_name = StringField("Last Name", validators=[DataRequired()], render_kw={"placeholder": "Last Name"})
    personal_id_number = StringField("Personal ID Number", validators=[DataRequired(), Length(11,11, message="Personal ID Number has 11 digits")])
    email = StringField("Email", validators=[DataRequired()], render_kw={"placeholder": "ex: xyz@gmail.com"})
    phone_number = StringField("Phone Number", validators=[DataRequired()], render_kw={"placeholder": "Phone Number"})
    city = StringField("City", validators=[DataRequired()], render_kw={"placeholder": "City"})
    street_name = StringField("Adress Line 1", validators=[DataRequired()], render_kw={"placeholder": "1234 Main St"})
    street_number = StringField("Adress Line 2", validators=[DataRequired()], render_kw={"placeholder": "Apartment"})
    zip_code = StringField("Zip Code", validators=[DataRequired()], render_kw={"placeholder": "xx-xxx"})
    field_of_study = SelectField("Field of Study", validators=[DataRequired()], render_kw={"placeholder": "Select"})
    form_of_study = SelectField("Form of Study", validators=[DataRequired()], choices=["full-time", "part-time"], render_kw={"placeholder": "Select"})
    birth_date = DateField("Date of Birth", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("Apply")

class ChangeRole(FlaskForm):
    role = SelectField("Role", validators=[DataRequired()], choices=["user", "admin"], render_kw={"placeholder": "Select"})
    submit = SubmitField("Save", render_kw={"onclick": "edit()"})

class DeclineForm(FlaskForm):
    message = StringField("Message", render_kw={"placeholder": "Leave short message for candidate"})
    checkbox = BooleanField("May apply again")
    submit = SubmitField("Decline")
