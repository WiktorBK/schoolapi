from flask import Flask, render_template, make_response, flash, request
from db import db
from forms import StudentForm, ClassForm
from flask_migrate import Migrate
from models.student import StudentModel
from werkzeug.security import generate_password_hash, check_password_hash
from models.class_ import ClassModel


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Qwerty1%40@localhost/schoolsystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = "top_secret"

db.init_app(app)
@app.before_first_request
def create_tables():
     db.create_all()
migrate = Migrate(app, db)


@app.errorhandler(404)
def page_not_found(e):
     return render_template("404.html"), 404
@app.errorhandler(500)
def internal_server_error(e):
     return render_template("500.html"), 500


@app.route("/")
def home():
     classes = ClassModel.find_all()

     return render_template('index.html', classes=classes)

@app.route("/student/add", methods=["GET", "POST"])
def add_student():
    headers = {'Content-Type': 'text/html'}
    name = None
    form = StudentForm()
    classes = ClassModel.find_all()
    form.class_id.choices = [class_.class_id for class_ in classes]
    if form.validate_on_submit():
        student = StudentModel.find_by_id(form.personal_id_number.data)
        if student is None:
            student = StudentModel(form.personal_id_number.data, form.name.data, form.surname.data, form.class_id.data)
            student.save_to_db()
            name = form.name.data
            form.name.data = ''
            form.surname.data= ''
            form.class_id.data = ''
            flash("Student Added Successfully")
    
    students = StudentModel.find_all()
    classes = ClassModel.find_all()
    return make_response(render_template("add_student.html", form=form,name=name, students=students, classes=classes), 200, headers)

@app.route("/update/<string:personal_id_number>", methods=['GET', 'POST'])
def update(personal_id_number):
     form = StudentForm()
     name = None
     student_to_update = StudentModel.query.get_or_404(personal_id_number)
     classes = ClassModel.find_all()
     form.class_id.choices = [class_.class_id for class_ in classes]
     if request.method == "POST":
          student = StudentModel.find_by_id(request.form['personal_id_number'])
          if student is None or request.form['personal_id_number'] == student_to_update.personal_id_number:
               student_to_update.name = request.form['name']
               student_to_update.surname = request.form['surname']
               student_to_update.class_id = request.form['class_id']
               student_to_update.personal_id_number = request.form['personal_id_number']
               try:
                    db.session.commit()
                    students = StudentModel.find_all()
                    flash("Student Updated Successfully!")
                    form.name.data = ''
                    form.surname.data= ''
                    form.class_id.data = ''
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

@app.route("/students/<string:class_id>")
def students(class_id):
     students = StudentModel.find_by_class(class_id)
     return render_template("students.html", students=students)

@app.route("/class/add", methods=["GET", "POST"])
def add_class():
     form = ClassForm()
     class_id = None
     if form.validate_on_submit():
        class_ = ClassModel.find_by_id(form.class_id.data)
        if class_ is None:
            class_id = form.class_id.data
            class_ = ClassModel(form.class_id.data)
            class_.save_to_db()
            form.class_id.data = ''
            flash("Class Added Successfully")
    
     classes = ClassModel.find_all()

     return render_template("add_class.html", class_id=class_id, form=form, classes=classes)

@app.route("/class/<string:class_id>")
def class_(class_id):
     class_ = ClassModel.query.get_or_404(class_id)
     classes = ClassModel.find_all()
     students = StudentModel.find_by_class(class_id)
     return render_template('class.html', class_ = class_, classes=classes, students=students)

@app.route("/class/<string:class_id>/student/add", methods=['GET', 'POST'])
def add_student_to_class(class_id):
     name = None
     form = StudentForm()
     form.class_id.choices = [class_id]
     if form.validate_on_submit():
        student = StudentModel.find_by_id(form.personal_id_number.data)
        if student is None:
            student = StudentModel(form.personal_id_number.data, form.name.data, form.surname.data, form.class_id.data)
            student.save_to_db()
            name = form.name.data
            form.name.data = ''
            form.surname.data= ''
            form.class_id.data = ''
            flash("Student Added Successfully")
     class_ = ClassModel.query.get_or_404(class_id)           
     return render_template("add_student_toclass.html",form = form, name= name,class_ = class_)


if __name__ == '__main__':
    app.run(port = 5000, debug=True)

