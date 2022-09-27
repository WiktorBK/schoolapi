from importlib.resources import Resource
from flask_restful import Api, Resource, reqparse
from flask import Flask, render_template
from db import db
from resources.student import Student, Students
from resources.class_ import Class, Classes
from resources.grade import Grade, StudentGrades, Grades


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
db.init_app(app)
@app.before_first_request
def create_tables():
     db.create_all()



api.add_resource(Student, "/student/<string:personal_id_number>")
api.add_resource(Students, "/students")
api.add_resource(Class, "/class/<string:name>")
api.add_resource(Classes, "/classes")
api.add_resource(Grade, "/student/<string:personal_id_number>/grade")
api.add_resource(StudentGrades, "/student/<string:personal_id_number>/grades")
api.add_resource(Grades, "/grades")

@app.errorhandler(404)
def page_not_found(e):
     return render_template("404.html"), 404
@app.errorhandler(500)
def internal_server_error(e):
     return render_template("500.html"), 500




if __name__ == '__main__':
    app.run(port = 5000, debug=True)

