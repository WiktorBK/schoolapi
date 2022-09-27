from flask_restful import Resource, reqparse
from models.student import StudentModel
from models.class_ import ClassModel
from flask import render_template, make_response


class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="Student needs a name")
    parser.add_argument("surname", type=str, required=True, help="Student needs a surname")
    parser.add_argument("class_", type=str, required=True, help="Student needs a class")

    def get(self, personal_id_number):
        headers = {'Content-Type': 'text/html'}
        student = StudentModel.find_by_id(personal_id_number)
        if student:
            return student.json()
        return make_response(render_template("student.html", personal_id_number=personal_id_number), 404, headers)
    
    def post(self, personal_id_number):
        data = Student.parser.parse_args()
        class_ = ClassModel.find_by_name(data['class_'])
        if StudentModel.find_by_id(personal_id_number):
            return {"message": "student with that personal id number already exists"}
        student = StudentModel(personal_id_number, **data)
        try:
            student.save_to_db()
        except:
            return {"message": "error occured while inserting the student"}, 500
        return student.json()
    
    def put(self, personal_id_number):
        data = Student.parser.parse_args()
        student = StudentModel.find_by_id(personal_id_number)
        if student is None:
            student = StudentModel(personal_id_number, **data)
        else:
            student.name = data['name']
            student.surname = data['surname']
            student.class_ = data['class_']

        student.save_to_db()

        return student.json()
            
    def delete(self, personal_id_number):
        student = StudentModel.find_by_id(personal_id_number)
        if student:
            student.delete_from_db()
            return {"message": "Student deleted"}
        return {"message": f"Student with that personal id number doesn't exist"}

class Students(Resource):
    def get(self):
        return {'Students': [student.json() for student in StudentModel.find_all()]}

