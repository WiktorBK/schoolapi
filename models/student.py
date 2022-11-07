
from re import I
from sqlalchemy import ForeignKey, func
from db import db
from models.fields import FieldModel
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, current_user

class StudentModel(db.Model, UserMixin):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.field_id'))
    personal_id_number = db.Column(db.String(11), nullable=False)
    first_name = db.Column(db.String(80))
    second_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    address1 = db.Column(db.String(80))
    address2 = db.Column(db.String(80))
    city = db.Column(db.String(80))
    zip_code = db.Column(db.String(80))
    form_of_study = db.Column(db.String(80))
    field_of_study = db.Column(db.String(80))
    phone_number = db.Column(db.String(80)) 
    field = db.relationship('FieldModel')
 


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
    def get_recent_student(cls):
        return db.session.query(func.max(cls.student_id)).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.order_by(cls.last_name)
    @classmethod
    def find_by_id(cls, student_id):
        return cls.query.filter_by(student_id=student_id).first()
     
    @classmethod 
    def find_by_field(cls, field_id):
        return cls.query.filter_by(field_id=field_id).order_by(cls.last_name)


