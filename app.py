from flask import Flask, render_template, make_response, flash, request, redirect, url_for, jsonify
from db import db
from forms import StudentForm, FieldForm, LoginForm, RegisterForm, ApplicationForm, ChangeRole
from flask_migrate import Migrate
from models.student import StudentModel
from werkzeug.security import generate_password_hash, check_password_hash
from models.fields import FieldModel
from models.user import UserModel
from flask_login import login_user, logout_user, LoginManager, login_required, current_user
from models.application import ApplicationModel
import pytz
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/schoolapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = "top_secret"


u = datetime.utcnow()
u = u.replace(tzinfo=pytz.utc)
print(u.astimezone(pytz.timezone("Europe/Berlin")).strftime('%d.%m.%Y %H:%M:%S'))


db.init_app(app)
@app.before_first_request
def create_tables():
     db.create_all()
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


def isadmin(user_id):
     if current_user.role == 'admin':
          return True
     else:
          return False

@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(int(id))

@app.errorhandler(404)
def page_not_found(e):
     return render_template("404.html"), 404
@app.errorhandler(500)
def internal_server_error(e):
     return render_template("500.html"), 500


@app.route("/admin")
@login_required
def admin():
     user_id = current_user.user_id
     if isadmin(user_id):
          return render_template('admin.html')
     else:
          return {"message": "access denied"}

@app.route("/")
def home():
     fields = FieldModel.find_all()

     return render_template('index.html', fields=fields)

@app.route("/register", methods=["GET", "POST"])
def register():
    headers = {'Content-Type': 'text/html'}
    name = None
    form = RegisterForm()
    if form.validate_on_submit():
        user = UserModel.find_by_email(form.email.data)
        if user is None:
            hashed_pw = generate_password_hash(form.password.data, "sha256")
            user = UserModel(form.name.data, form.surname.data, form.email.data, hashed_pw)
            user.save_to_db()
            name = form.name.data
            form.name.data = ''
            form.surname.data= ''
            form.email.data = ''
            form.password.data = ''
            form.password_repeat.data = ''
            flash("Account Created Successfully. Logged in automatically")
            login_user(user)
            if isadmin(current_user.user_id):
               return redirect(url_for('admin'))
            else:
               return redirect(url_for('dashboard'))
    
    users = UserModel.find_all()
    return make_response(render_template("register.html", form=form,name=name, users=users), 200, headers)

@app.route("/login", methods=["GET", "POST"])
def login():
     form = LoginForm()
     if form.validate_on_submit():
          user = UserModel.find_by_email(form.email.data)
          if user:
               if check_password_hash(user.password_hash, form.password.data):
                    login_user(user)
                    flash("Login Successfull!")
                    if isadmin(current_user.user_id):
                         return redirect(url_for('admin'))
                    else:
                         return redirect(url_for('dashboard'))
               else:
                    flash("Wrong Password - Try Again!")
          else:
               flash("That User Doesn't Exist - Try Again!")

     return render_template('login.html', form=form)


@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
     logout_user()
     flash("You Have Been Logged Out!")
     return redirect(url_for('login'))



@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
     application = ApplicationModel.find_by_user(current_user.user_id)
     return render_template('dashboard.html', application=application)

@app.route("/update/<string:personal_id_number>", methods=['GET', 'POST'])
def update(personal_id_number):
     form = StudentForm()
     name = None
     student_to_update = StudentModel.query.get_or_404(personal_id_number)
     fields = FieldModel.find_all()
     form.field_name.choices = [field.field for field in fields]
     form.field_form.choices = ["full-time", "part-time"]
     if request.method == "POST":
          student = StudentModel.find_by_id(request.form['personal_id_number'])
          if student is None or request.form['personal_id_number'] == student_to_update.personal_id_number:
               student_to_update.name = request.form['name']
               student_to_update.surname = request.form['surname']
               student_to_update.field_name = request.form['field_name']
               student_to_update.field_form = request.form['field_form']
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
     field = FieldModel.find_field(student_to_delete.field_id)
     fields = FieldModel.find_all()
     name = None
     form = StudentForm()
     try:
          student_to_delete.delete_from_db()
          students = StudentModel.find_all()
          flash("Student Deleted Successfully")
          return render_template("field.html",students=students, field=field, fields=fields)
     except:
          flash("Student could not be deleted") 
          return render_template("field.html",students=students,  field=field, fields=fields)  



@app.route("/field/add", methods=["GET", "POST"])
@login_required
def add_field():
     if isadmin(current_user.user_id):
          form = FieldForm()
          field_name = None
          form.form.choices = ["full-time", "part-time"]
          if form.validate_on_submit():
               field = FieldModel.find_by_name(form.field.data, form.form.data)
               if field is None:
                    field_name = form.field.data
                    field = FieldModel(form.field.data, form.form.data, form.capacity.data)
                    field.save_to_db()
                    form.field.data = ''
                    form.capacity.data = ''
                    flash("Field Added Successfully")
     
          
          fields = FieldModel.find_all()
  
          return render_template("add_field.html", field=field_name, form=form, fields=fields, )
     else:
          return {"message": "access denied"}
          
@app.route("/field/<form>") 
def field_(form):
     fields = FieldModel.find_all_in_form(form)

     fieldsList = []

     for field in fields:
          fieldObj = {}
          fieldObj['name'] = field.field
          fieldsList.append(fieldObj) 

     return jsonify({'fields':fieldsList})     

@app.route("/field/<int:field_id>", methods=["GET", "POST"])
@login_required
def field(field_id):
     if isadmin(current_user.user_id):
          field = FieldModel.query.get_or_404(field_id)
          fields = FieldModel.find_all()
          students = StudentModel.find_by_field(field_id)
          return render_template('field.html', field = field, fields=fields, students=students)
     else:
          return {"message": "access denied"}     
     
@app.route("/fields")
@login_required
def fields():
     if isadmin(current_user.user_id): 
          fields = FieldModel.find_all()
          fulltime = FieldModel.find_all_in_form("full-time")
          parttime = FieldModel.find_all_in_form("part-time")    
          return render_template("fields.html", fields = fields, fulltime=fulltime, parttime=parttime)
     else:
          return {"message": "access denied"}     

@app.route("/get_data")
def get_data():
     fields = FieldModel.find_all()
     applications = ApplicationModel.find_all()
     students = ApplicationModel.find_accepted()
     users = UserModel.find_all()
     field_count = 0
     application_count = 0
     student_count = 0
     user_count = 0
     for field in fields:
          field_count += 1
     for application in applications:
          application_count += 1
     for student in students:
          student_count += 1   
     for user in users:
          user_count += 1            

     return jsonify({'field_count':field_count, 'application_count': application_count, 'student_count': student_count, 'user_count': user_count})  

@app.route("/field/<int:field_id>/student/add", methods=['GET', 'POST'])
def add_student_to_class(field_id):
     name = None
     form = StudentForm()
     field = FieldModel.query.get_or_404(field_id)    
     form.field_name.choices = [field.field]
     form.field_form.choices = [field.form]
     if form.validate_on_submit():
        student = StudentModel.find_by_id(form.personal_id_number.data)
        if student is None:
            student = StudentModel(form.personal_id_number.data, form.name.data, form.surname.data, field.field_id)
            student.save_to_db()
            name= form.name.data
            form.name.data = ''
            form.surname.data= ''
            form.field_name.data = ''
            form.field_form.data = ''
            flash("Student Added Successfully")
            students = StudentModel.find_by_field(field_id)
            return render_template("field.html",form = form, name= name, field = field, students = students)       
     return render_template("add_student_toclass.html",form = form, name= name,field = field)

@app.route("/students")
def students():
     students = StudentModel.find_all()
     return render_template("students.html", students = students)



@app.route("/apply", methods=["GET", "POST"])
@login_required
def application():
     form = ApplicationForm()
     name = None
     fields = FieldModel.find_all_in_form("full-time")
     form.field_of_study.choices = [field.field for field in fields]
     already_sent = ApplicationModel.already_sent(current_user.user_id)
     application = ApplicationModel.find_by_user(current_user.user_id)
     if already_sent == False:
          if form.validate_on_submit():
               already_sent = True
               application = ApplicationModel(user_id = current_user.user_id, 
               first_name = form.first_name.data,
               second_name = form.second_name.data,
               last_name = form.last_name.data,
               email = form.email.data,
               birth_date = form.birth_date.data,
               phone_number = form.phone_number.data,
               personal_id_number = form.personal_id_number.data,
               address1 = form.street_name.data,
               address2 = form.street_number.data,
               city = form.city.data,
               zip_code = form.zip_code.data,
               form_of_study = form.form_of_study.data,
               field_of_study = form.field_of_study.data,
               )

               application.save_to_db()
               
               form.first_name.data = ''
               form.second_name.data= ''
               form.last_name.data= ''
               form.email.data= ''
               form.birth_date.data = ''
               form.phone_number.data= ''
               form.street_name.data= ''
               form.street_number.data= ''
               form.city.data= ''
               form.zip_code.data= ''
               form.form_of_study.data= ''
               form.field_of_study.data= ''
               form.personal_id_number.data = ''
          
            
     return render_template('application.html', form=form, already_sent=already_sent, application=application)

@app.route("/applications")
@login_required
def applications():
     if isadmin(current_user.user_id):
          applications = ApplicationModel.find_all_active()
          return render_template("show_applications.html", applications = applications)
     else:
          return{"message": "access denied"}

@app.route("/application/<int:application_id>/accept")
def application_accept(application_id):
     if isadmin(current_user.user_id):
          application = ApplicationModel.find_by_id(application_id)
          if application.status == "to_review":
               user = UserModel.find_by_id(application.user_id)
               recent = StudentModel.get_recent_student()[0]
               if recent:
                    student_id = recent + 1
               else:
                    student_id = 1     
               student = StudentModel( 
                    user_id = application.user_id,
                    student_id = student_id,                   
                    first_name = application.first_name,
                    personal_id_number = application.personal_id_number,
                    second_name = application.second_name,
                    last_name = application.last_name,
                    email = application.email,
                    birth_date = application.birth_date,
                    address1 = application.address1,
                    address2 = application.address2,
                    city = application.city,
                    zip_code = application.zip_code,
                    form_of_study = application.form_of_study,
                    field_of_study = application.field_of_study,
                    field_id = FieldModel.find_by_name(application.field_of_study, application.form_of_study).field_id,
                    phone_number = application.phone_number
               )
               application.status = "accepted"
               db.session.commit()
               student.save_to_db()
               flash("Application has been accepted")     
          applications = ApplicationModel.find_all_active()
          return render_template('show_applications.html', applications=applications)
     else:
          return{"message": "access denied"}

@app.route("/application/<int:application_id>/decline")
def application_decline(application_id):
    if isadmin(current_user.user_id):
          application = ApplicationModel.find_by_id(application_id)
          if application.status == "to_review":
               application.status = "declined"
               application.save_to_db()
               flash("Application has been declined")
          applications = ApplicationModel.find_all_active()        
          return render_template('show_applications.html', applications=applications)
    else:
          return{"message": "access denied"}

@app.route("/application/<int:application_id>/details")
def application_details(application_id):
    if isadmin(current_user.user_id):
       application = ApplicationModel.find_by_id(application_id)
    else:
        application = ApplicationModel.find_by_user(current_user.user_id)
    if isadmin(current_user.user_id) or application and application_id == application.application_id:
          return render_template("application_details.html", application=application)
    else:
      return{"message": "access denied"}

@app.route("/users")
def users():
     users = UserModel.find_all()
     form = ChangeRole()
     return render_template('users.html', users=users, form=form)

@app.route("/user/<int:user_id>", methods=["GET", "POST"])
def user(user_id):
     user = UserModel.find_by_id(user_id)
     application = ApplicationModel.find_by_user(user_id)
     student = StudentModel.find_by_user(user_id)
     form = ChangeRole()
     form.role.default = user.role
     form.process()
     if request.method == "POST":
          print('editing')
          if request.form["role"] is not None:
               user.role = request.form['role']
          try:
               db.session.commit()
               flash("User Updated Successfully!")
          except:
               flash("User couldn't be updated, try again...")

     return render_template('user.html', form=form, user=user, application=application, student=student)

@app.route("/student/<int:student_id>", methods=["GET", "POST"])
@login_required
def student(student_id):
     if isadmin(current_user.user_id):
          student = StudentModel.find_by_id(student_id)
          form = StudentForm()
          form.form_of_study.default = student.form_of_study
          form.field_of_study.default = student.field_of_study
          form.process()
          fields = FieldModel.find_all_in_form(student.form_of_study)
          form.field_of_study.choices = [field.field for field in fields]
          return render_template("student.html", student = student, form=form)
     else:
          return {"message": "access denied"}

@app.route("/delete/<int:user_id>")
def delete_user(user_id):
     print(f"{user_id} deleted")
     return {user_id: "deleted"}

                    

if __name__ == '__main__':
    app.run(port = 5000, debug=True)

