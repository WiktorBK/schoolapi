from flask_restful import Api, Resource
from flask import Flask, render_template, make_response, flash, request
from db import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from forms import StudentForm
from flask_migrate import Migrate
from models.student import StudentModel
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Qwerty1%40@localhost/schoolsystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = "top_secret"

db.init_app(app)
migrate = Migrate(app, db)


@app.errorhandler(404)
def page_not_found(e):
     return render_template("404.html"), 404
@app.errorhandler(500)
def internal_server_error(e):
     return render_template("500.html"), 500


@app.route("/")
def home():
     return render_template('index.html')

@app.route("/student/add", methods=["GET", "POST"])
def add_student():
    headers = {'Content-Type': 'text/html'}
    name = None
    form = StudentForm()
    if form.validate_on_submit():
        student = StudentModel.find_by_id(form.personal_id_number.data)
        if student is None:
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            student = StudentModel(form.personal_id_number.data, form.name.data, form.surname.data, form.class_.data, hashed_pw)
            student.save_to_db()
            name = form.name.data
            form.name.data = ''
            form.surname.data= ''
            form.class_.data = ''
            form.personal_id_number.data = ''
            form.password_hash.data = ''
            form.password_hash2.data = ''
            flash("Student Added Successfully")
    
    students = StudentModel.find_all()

    return make_response(render_template("add_student.html", form=form,name=name, students=students), 200, headers)

@app.route("/update/<string:personal_id_number>", methods=['GET', 'POST'])
def update(personal_id_number):
     form = StudentForm()
     name = None
     student_to_update = StudentModel.query.get_or_404(personal_id_number)
     if request.method == "POST":
          student = StudentModel.find_by_id(request.form['personal_id_number'])
          if student is None or request.form['personal_id_number'] == student_to_update.personal_id_number:
               student_to_update.name = request.form['name']
               student_to_update.surname = request.form['surname']
               student_to_update.class_ = request.form['class_']
               student_to_update.personal_id_number = request.form['personal_id_number']
               try:
                    db.session.commit()
                    students = StudentModel.find_all()
                    flash("Student Updated Successfully!")
                    form.name.data = ''
                    form.surname.data= ''
                    form.class_.data = ''
                    form.personal_id_number.data = ''
                    return render_template("students.html", students=students)
               except:
                    flash("Student couldn't be updated, try again...")
                    return render_template("update_student.html", form=form, student_to_update=student_to_update, personal_id_number=personal_id_number)
          else:
               flash("Student with that Personal ID Number already exists")
               return render_template("update_student.html", form=form, student_to_update=student_to_update,  personal_id_number=personal_id_number)
                           
     else:
           return render_template("update_student.html", form=form, student_to_update=student_to_update, personal_id_number=personal_id_number)

@app.route("/delete/<string:personal_id_number>")
def delete(personal_id_number):
     student_to_delete = StudentModel.query.get_or_404(personal_id_number)
     name = None
     form = StudentForm()
     try:
          student_to_delete.delete_from_db()
          students = StudentModel.find_all()
          flash("Student Deleted Successfully")
          return render_template("students.html",students=students)
     except:
          flash("Student could not be deleted") 
          return render_template("students.html",students=students)  

@app.route("/students")
def students():
     students = StudentModel.find_all()
     return render_template("students.html", students=students)



if __name__ == '__main__':
    app.run(port = 5000, debug=True)

