from flask_restful import Resource, reqparse
from models.grade import GradeModel
from models.student import StudentModel
from flask import render_template, make_response

class Grade(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('subject', type=str, required = True, help="Field 'subject' cannot be left blank")
    parser.add_argument('grade', type=str, required = True, help="Field 'grade' cannot be left blank")

    def post(self, personal_id_number):
        data = Grade.parser.parse_args()
        student = StudentModel.find_by_id(personal_id_number)
        if student:
            grade = GradeModel(personal_id_number, **data)
            try:
                grade.save_to_db()
            except:
                return {"message": "error occured while inserting the grade"}, 500
            return grade.json()
        return {"message": "student with that personal id number doesn't exist"}
    
    def delete(self, personal_id_number):
        data = Grade.parser.parse_args()
        student = StudentModel.find_by_id(personal_id_number)
        if student:
            grade = GradeModel.find_grade(**data)
            if grade:
                grade.delete_from_db()
                return {"message": "Grade has been deleted"}
            return {"message": "This student has no such grade"}
        return {"message": "Student with that personal id number doesn't exist"}

class StudentGrades(Resource):  
    def get(self, personal_id_number):
        student = StudentModel.find_by_id(personal_id_number)
        if student:
            print(GradeModel.get_students_avg(personal_id_number, 'wf'))
            return {"grades": [grade.json() for grade in GradeModel.get_students_grades(personal_id_number)]}
        # headers = {'Content-Type': 'text/html'}
        # return make_response(render_template("index.html"), 200, headers)
    
class Grades(Resource):  
    def get(self):
        return {"grades": [grade.json() for grade in GradeModel.find_all()]}

class GradeAvg(Resource):
    def get(self, personal_id_number, subject):
        return {f"{subject}": ""}