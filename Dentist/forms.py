from flask_wtf import FlaskForm
from flask_login import current_user
from flask_admin.contrib.sqla.fields import QuerySelectField
from wtforms import StringField, StringField, PasswordField, SelectField, validators, ValidationError, SubmitField, IntegerField, DateField, HiddenField, TextAreaField
from wtforms.validators import Email, DataRequired, EqualTo
from flask_wtf.file import FileAllowed, FileField
from .models import Patient, Dentist, Book
from .tools import verify_pass

class PatientForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'),('Female', 'Female')])
    age = IntegerField('Age', [validators.NumberRange(min=1, max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired(),
                                         EqualTo('confirm',
                                                 message='invalid password')])
    confirm = PasswordField("Repeat Password", [validators.DataRequired()])
    address = StringField('Address', [validators.DataRequired()])
    phone = StringField('Phone', [validators.DataRequired()])
    
    submit = SubmitField("Register")

    def validate_email(self, email):
        if Patient.query.filter_by(email=email.data).first():
            raise ValidationError("Email already Exists.")
        
        
class DentistForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired(),
                                         EqualTo('confirm',
                                                 message='invalid password')])
    confirm = PasswordField("Repeat Password", [validators.DataRequired()])
    phone = StringField('Phone', [validators.DataRequired()])


    submit = SubmitField("Register")

    def validate_email(self, email):
        if Patient.query.filter_by(email=email.data).first():
            raise ValidationError("Email already Exists.")



class LoginForm(FlaskForm):
    email = StringField("Email", validators=[validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])  
    submit = SubmitField('Login')

def get_dentist_label(dentist):
    return f"{dentist.name}"

class BookForm(FlaskForm):
    patient_id = IntegerField('Patient Id',
                           validators=[DataRequired()])
    dentist_id =  QuerySelectField("Name of Dentist",
                                  query_factory=lambda: Dentist.query.order_by(Dentist.name).all(),
                                  get_label=get_dentist_label)
    date=DateField('Choose date', format="%m/%d/%Y",validators=[DataRequired()])
    time = SelectField('Time', choices=[('9AM', '9AM'),('11AM', '11AM')])
    