from ast import ClassDef
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, SelectField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length

class StudentForm(FlaskForm):
    personal_id_number = StringField("Personal ID Number", validators=[DataRequired(), Length(11,11, message="Personal ID Number has 11 digits")])
    name = StringField("First Name", validators=[DataRequired()])
    surname = StringField("Last Name", validators=[DataRequired()])
    field_name = SelectField("Field", validators=[DataRequired()])
    field_form = SelectField("Form", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class FieldForm(FlaskForm):
    field = StringField("Field", validators=[DataRequired()])
    form = SelectField("Form", validators=[DataRequired()])
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
    email = StringField("Email", validators=[DataRequired()], render_kw={"placeholder": "ex: xyz@gmail.com"})
    phone_number = StringField("Phone Number", validators=[DataRequired()], render_kw={"placeholder": "Phone Number"})
    city = StringField("City", validators=[DataRequired()], render_kw={"placeholder": "City"})
    street_name = StringField("Adress Line 1", validators=[DataRequired()], render_kw={"placeholder": "1234 Main St"})
    street_number = StringField("Adress Line 2", validators=[DataRequired()], render_kw={"placeholder": "Apartment"})
    zip_code = StringField("Zip Code", validators=[DataRequired()], render_kw={"placeholder": "xx-xxx"})
    field_of_study = SelectField("Field Of Study", validators=[DataRequired()], render_kw={"placeholder": "Select"})
    form_of_study = SelectField("Form Of Study", validators=[DataRequired()], choices=["full-time", "part-time"], render_kw={"placeholder": "Select"})
    submit = SubmitField("Apply")

