from ast import ClassDef
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, SelectField
from wtforms.validators import DataRequired, EqualTo, Length

class StudentForm(FlaskForm):
    personal_id_number = StringField("Personal ID Number", validators=[DataRequired(), Length(11, 11, "Personal ID Number has 11 digits")])
    name = StringField("First Name", validators=[DataRequired()])
    surname = StringField("Last Name", validators=[DataRequired()])
    class_id = SelectField("Class", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class ClassForm(FlaskForm):
    class_id = StringField("Class", validators=[DataRequired()])
    submit = SubmitField("Submit")