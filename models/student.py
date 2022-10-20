
from db import db
from models.fields import FieldModel
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, current_user

class StudentModel(db.Model, UserMixin):
    __tablename__ = 'students'
    personal_id_number = db.Column(db.String(11), nullable=False, primary_key=True, autoincrement=False)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.field_id'))  
    field = db.relationship('FieldModel') 




    def __init__(self, personal_id_number, name, surname, field_id):
        self.personal_id_number = personal_id_number
        self.name = name
        self.surname = surname
        self.field_id = field_id


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
     
    @classmethod 
    def find_by_field(cls, field_id):
        return cls.query.filter_by(field_id=field_id).order_by(cls.surname)
