from flask import send_from_directory, render_template, url_for, flash, redirect, request, jsonify, abort, current_app, session
from flask_login import login_user, current_user, logout_user, login_required
from Dentist import app, db, bcrypt, photos
from Dentist.models import User, Patient, Dentist, Book
from Dentist.forms import PatientForm, LoginForm, DentistForm, BookForm
@app.route('/', strict_slashes=False)
@app.route('/home', strict_slashes=False)
def home():
    return render_template('home.html')



@app.route('/signup', methods=["POST", "GET"])
def signup():
    msg = ""
    form  = PatientForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        patient = Patient(name=form.name.data, gender=form.gender.data,
                age=form.age.data, email=form.email.data,
                password=hash_password, address=form.address.data,
                phone=form.phone.data)
        db.session.add(patient)
        db.session.commit()
        msg = "Welcome:{form.name.data} Thank Your for Registering, success"
        return redirect(url_for('loginPatient'))
    return render_template('signup.html', form=form, msg=msg)


@app.route('/loginPatient', methods=['GET', "POST"])
def loginPatient():
    msg = ""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        patient = Patient.query.filter_by(email=form.email.data).first()
        if patient and bcrypt.check_password_hash(patient.password, form.password.data):
            login_user(patient, remember=True)
            return redirect(url_for('home'))
        else:
            msg = 'Login unsuccessful, please check your credentials and try again'
    return render_template('loginPatient.html', msg=msg, form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route('/loginAdmin', methods=['GET', "POST"])
def loginAdmin():
    msg = ""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.is_admin:
            login_user(user, remember=True)
            return redirect(url_for('dashboard'))
        else:
            msg = 'Login unsuccessful, please check your credentials and try again'
    return render_template('loginAdmin.html', msg=msg, form=form)


@app.route('/logoutAdmin')
def logoutAdmin():
    logout_user()
    return redirect(url_for('loginAdmin'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/addDentist', methods=["GET", "POST"])
def addDentist():
    msg = ""
    form = DentistForm()
    if request.method == "POST":
        name = form.name.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data)
        phone = form.phone.data
        dentist = Dentist(name=name, email=email, password=password, 
        phone=phone)
        db.session.add(dentist)
        db.session.commit()
        msg = "Dentist has been added"
        return redirect(url_for('dentists'))
    return render_template('add_dentist.html', form=form, msg=msg)



@app.route('/loginDentist', methods=['GET', "POST"])
def loginDentist():
    msg = ""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        dentist = Dentist.query.filter_by(email=form.email.data).first()
        if dentist and bcrypt.check_password_hash(dentist.password, form.password.data):
            login_user(dentist, remember=True)
            return redirect(url_for('dashboard'))
        else:
            msg = 'Login unsuccessful, please check your credentials and try again'
    return render_template('loginDentist.html', msg=msg, form=form)


@app.route('/dentists')
def dentists():
    dentists = Dentist.query.all()
    return render_template('dentists.html', dentists=dentists)

@app.route('/patients')
def patients():
    patients = Patient.query.all()
    return render_template('patients.html', patients=patients)


@app.route('/addBook', methods=["GET", "POST"])
def addBook():
    msg = ""
    form = BookForm()
    if current_user.is_authenticated:
        form.patient_id.default = current_user.name
        form.process()

    if form.validate_on_submit():
        patient_id= current_user.name if current_user.is_authenticated else None
        dentist_id = form.dentist_id.data
        date = form.date.data
        time = form.time.data
        book = Book(patient_id=patient_id, dentist_id=dentist_id, date=date, 
        time=time)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_book.html', form=form, msg=msg)