from db import db
from werkzeug.security import generate_password_hash, check_password_hash

class FieldModel(db.Model):
    __tablename__ = 'fields'
    field_id = db.Column(db.Integer, primary_key=True)
    form = db.Column(db.String(80))
    field = db.Column(db.String(80))
    students = db.relationship('StudentModel', backref='student', lazy='dynamic')
  
    @classmethod
    def find_by_name(cls, field_name, field_form):
        return cls.query.filter_by(form=field_form).filter_by(field=field_name).first()

    def __init__(self,field, form):
        self.field = field
        self.form = form
     
    @classmethod
    def find_all(cls):
        return cls.query.order_by()
    @classmethod
    def find_all_in_form(cls, form):
        return cls.query.filter_by(form=form).order_by(cls.field)

    @classmethod
    def find_field(cls, field_id):
        return cls.query.filter_by(field_id=field_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()    
