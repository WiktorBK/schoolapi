from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from models.class_ import ClassModel

class StudentModel(db.Model):
    __tablename__ = 'students'
    personal_id_number = db.Column(db.String(9), primary_key=True, autoincrement=False)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    class_id = db.Column(db.String(3), db.ForeignKey(ClassModel.class_id))   
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __init__(self, personal_id_number, name, surname, class_id, password):
        self.personal_id_number = personal_id_number
        self.name = name
        self.surname = surname
        self.class_id = class_id
        self.password = password

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
        return cls.query.order_by(cls.surname)
    @classmethod
    def find_by_id(cls, personal_id_number):
        return cls.query.filter_by(personal_id_number=personal_id_number).first()
