from db import db

class StudentModel(db.Model):
    __tablename__ = 'students'
    personal_id_number = db.Column(db.String(9), primary_key=True, autoincrement=False)
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    class_ = db.Column(db.String(3), db.ForeignKey('classes.class_'))
    class_name = db.relationship('ClassModel')
    

    def __init__(self, personal_id_number, name, surname, class_):
        self.personal_id_number = personal_id_number
        self.name = name
        self.surname = surname
        self.class_ = class_

    def json(self):
        return {"personal_id_number": self.personal_id_number,
                "name": self.name,
                "surname": self.surname,
                "class": self.class_
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
    def find_by_id(cls, personal_id_number):
        return cls.query.filter_by(personal_id_number=personal_id_number).first()
