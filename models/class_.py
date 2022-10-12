from db import db
from werkzeug.security import generate_password_hash, check_password_hash

class ClassModel(db.Model):
    __tablename__ = 'classes'
    class_id = db.Column(db.String(3), primary_key=True)
    students = db.relationship('StudentModel', backref='student', lazy='dynamic')
  
    @classmethod
    def find_by_id(cls, class_id):
        return cls.query.filter_by(class_id=class_id).first()

    def __init__(self, class_id):
        self.class_id = class_id
     

    @classmethod
    def find_all(cls):
        return cls.query.order_by(cls.class_id)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()    
