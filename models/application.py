from db import db
from datetime import datetime 
import pytz

class ApplicationModel(db.Model):
    __tablename__ = "applications"
    application_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) 
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
    birth_date = db.Column(db.String(80))
    u = datetime.utcnow()
    u = u.replace(tzinfo=pytz.utc)
    date = db.Column(db.DateTime, default=u.astimezone(pytz.timezone("Europe/Berlin")).strftime('%d.%m.%Y %H:%M:%S'))
    status = db.Column(db.String(80), default="to_review")
    message = db.Column(db.String(1000))
    mayapply = db.Column(db.Boolean)
    user = db.relationship('UserModel')  

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all_active(cls):
        return cls.query.filter_by(status="to_review").order_by(cls.application_id)
    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_accepted(cls):

        return cls.query.filter_by(status="accepted").order_by(cls.application_id)    
    @classmethod
    def already_sent(cls, user_id):
        if cls.query.filter_by(user_id=user_id).first():
            return True
        else:
            return False

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, application_id):
        return cls.query.filter_by(application_id=application_id).first()

    @classmethod
    def find_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
