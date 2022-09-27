from db import db

class ClassModel(db.Model):
    __tablename__ = "classes"
    class_ = db.Column(db.String(3), primary_key = True, autoincrement = False) 
    students = db.relationship('StudentModel', lazy='dynamic')

    def __init__(self, class_):
        self.class_ = class_

    def json(self):
        return {
            "class": self.class_,
            'students': [student.json() for student in self.students.all()]
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(class_=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()