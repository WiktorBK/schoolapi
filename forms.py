from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length

class StudentForm(FlaskForm):
    personal_id_number = StringField("Personal ID Number", validators=[DataRequired()])
    name = StringField("First Name", validators=[DataRequired()])
    surname = StringField("Last Name", validators=[DataRequired()])
    class_ = StringField("Class", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Password Must Match!')])
    password_hash2 = PasswordField("Confirm Password",validators=[DataRequired()])
    submit = SubmitField("Submit")
    
