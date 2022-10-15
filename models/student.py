from tabnanny import check
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from models.class_ import ClassModel
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, current_user

class StudentModel(db.Model, UserMixin):
    __tablename__ = 'students'
    personal_id_number = db.Column(db.String(11), nullable=False, primary_key=True, autoincrement=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    class_id = db.Column(db.String(3), db.ForeignKey('classes.class_id'))  
    class_ = db.relationship('ClassModel') 
    password_hash = db.Column(db.String(128))


    @property
    def password(self):  
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __init__(self, personal_id_number, name, surname, email, class_id, password_hash):
        self.personal_id_number = personal_id_number
        self.name = name
        self.surname = surname
        self.class_id = class_id
        self.email = email
        self.password_hash = password_hash

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
    def find_by_class(cls, class_id):
        return cls.query.filter_by(class_id=class_id).order_by(cls.surname)
