from ast import ClassDef
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, SelectField
from wtforms.validators import DataRequired, EqualTo, Length

class StudentForm(FlaskForm):
    personal_id_number = StringField("Personal ID Number", validators=[DataRequired(), Length(11, 11, "Personal ID Number has 11 digits")])
    email = StringField("Email", validators=[DataRequired()])
    name = StringField("First Name", validators=[DataRequired()])
    surname = StringField("Last Name", validators=[DataRequired()])
    class_id = SelectField("Class", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('passsword_repeat')])
    password_repeat = PasswordField("Repeat Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class ClassForm(FlaskForm):
    class_id = StringField("Class", validators=[DataRequired()])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Last Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_repeat = PasswordField("Repeat Password", validators=[DataRequired()])
    submit = SubmitField("Submit")