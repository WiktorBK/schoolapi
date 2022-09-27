from db import db
from sqlalchemy.sql import func, select


class GradeModel(db.Model):
    __tablename__ = 'grades'
    grade_id = db.Column(db.Integer, primary_key=True)
    personal_id_number = db.Column(db.String(12), db.ForeignKey('students.personal_id_number'))
    subject = db.Column(db.String(80))
    grade = db.Column(db.Integer())

    def __init__(self, personal_id_number, subject, grade):
        self.subject = subject
        self.grade = grade
        self.personal_id_number = personal_id_number

    def json(self):
        return {
            "student's personal id number": self.personal_id_number,
            "subject": self.subject,
            "grade":   self.grade
        }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    @classmethod
    def find_all(cls):
        return cls.query.all()
    @classmethod
    def find_grade(cls, subject, grade):
        return cls.query.filter_by(subject=subject).filter_by(grade=grade).first()
    @classmethod
    def get_students_grades(cls, personal_id_number):
        return cls.query.filter_by(personal_id_number=personal_id_number).all()
    @classmethod
    def get_students_avg(cls, personal_id_number, subject):
        pass