from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from models.fields import FieldModel
from models.application import ApplicationModel
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, current_user

class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(80))
    role = db.Column(db.String(80), default = 'user')
    applications = db.relationship('ApplicationModel', backref='application', lazy='dynamic')
    
    @property
    def password(self):  
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, name, surname, email, password_hash):
        self.name = name
        self.surname = surname
        self.email = email
        self.password_hash = password_hash
        
    def get_id(self):
           return (self.user_id)
           
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    @classmethod
    def find_all(cls):
        return cls.query.order_by(cls.role).all()
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
     