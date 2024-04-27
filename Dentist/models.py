from Dentist import db, login_manager
from flask_login import UserMixin
from .tools import hash_pass

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

    
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(500), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    patient_user = db.relationship("Patient", backref="user", cascade="all, delete, delete-orphan")
    dentist_user = db.relationship("Dentist", backref="user", cascade="all, delete, delete-orphan")


class Patient(User):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    gender = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=False)
    phone = db.Column(db.String(120), unique=False, nullable=False)

    book_item = db.relationship("Book", backref="patient_book", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"Patient('{self.username}', '{self.email}')"
    
class Dentist(User):
    __tablename__ = 'dentists'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    phone = db.Column(db.String(120), unique=False, nullable=False)

    book_item = db.relationship("Book", backref="dentist_book", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"Doctor('{self.name}')"
    

class Book(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    dentist_id = db.Column(db.Integer, db.ForeignKey('dentists.id'))
    date=db.Column(db.DateTime, nullable=False)
    time = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default="pending")