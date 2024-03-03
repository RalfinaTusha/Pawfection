from flask_app import app
from flask import jsonify, render_template, redirect, session, request, flash
from flask_app.models.admin import Admin
from flask_app.models.user import User
from flask_app.models.vet import Vet
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import os   
from datetime import datetime
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'flask_app/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return redirect('/loginpage')

@app.route('/loginpage')
def loginPage():
    if 'user_id' in session:
        return redirect('/')
    
    return render_template('login.html')

@app.route('/dashboard')
def all_users():
    if 'user_id' not in session:
        return redirect('/')
    loggedUserData = {
        'user_id': session['user_id']
    } 
    loggedUser = User.get_user_by_id(loggedUserData)
    animals=User.get_animals_of_user(loggedUserData)
    if not loggedUser:
        return redirect('/logout')
    return render_template('index.html', loggedUser=loggedUser,animals=animals)


 
@app.route('/register', methods=['POST'])
def register():
    if 'user_id' in session:
        return redirect('/')
    if User.get_user_by_email(request.form):
        flash('This email already exists. Try another one.', 'emailSignUp')
        return redirect(request.referrer)
    if not User.validate_user(request.form):
        return redirect(request.referrer)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'confirm_password': request.form['confirm_password']
    }
    user_id = User.create_user(data)

    session['user_id'] = user_id

    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    if 'user_id' in session:
        return redirect('/')
    user = User.get_user_by_email(request.form)
    if not user:
        flash('This email does not exist.', 'emailLogin')
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash('Your password is wrong!', 'passwordLogin')
        return redirect(request.referrer)
    session['user_id'] = user['id']
    return redirect('/')

@app.route('/contact')
def contact():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('contact.html')

@app.route('/services')
def services():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('services.html')


@app.route('/prices')
def prices():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('pricing.html')


@app.route('/vets')
def vets():
    if 'user_id' not in session:
        return redirect('/')
    vets= Vet.get_all_vets()
    return render_template('vet.html',vets=vets)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id": session['user_id']
    }
    user = User.get_user_by_id(data)
    animals = User.get_animals_of_user(data)
    vets = Vet.get_all_vets()
    return render_template('profile.html', user = user, animals = animals, vets = vets)


@app.route('/addanimal', methods=['POST'])
def add_animal():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id": session['user_id'],
        "name": request.form['name'],
        "species": request.form['species'],
        "age": request.form['age'],
        "vet_id": request.form['vet_id']
    }
    User.add_animal(data)
    return redirect('/profile')


@app.route('/profilepic/user', methods=['POST'])
def new_profil_pic_user():
    if 'user_id' not in session:
        return redirect('/loginpage')
    
    data = {"id": session['user_id']}
    
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data['image'] = filename
            User.update_profile_pic_user(data)
    return redirect('/profile')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/loginpage')

#add appointment
@app.route('/addappointment', methods=['POST'])
def add_appointment():
    if 'user_id' not in session:
        return redirect('/loginpage')
    service = request.form['service']
    vet_id = Vet.get_vet_id_based_on_service(service)
    data = {
        "user_id": session['user_id'],
        'name': request.form['name'],
        "date": request.form['date'],
        "time": request.form['time'],
        'service': request.form['service'],
        'message': request.form['message'],
        'vet_id': vet_id
    }
    User.add_appointment(data)
    return redirect('/')


@app.route("/sendmessage", methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id": session['user_id'],
        "subject": request.form['subject'],
        "message": request.form['message'],
        "admin_id": "1"
    }
    User.send_message(data)
    return redirect('/contact')

@app.route("/adoptanimals")
def adoptanimals():
    if 'user_id' not in session:
        return redirect('/loginadminpage')
    adoptanimals=Admin.get_all_adoptanimals()
    return render_template('adoptanimals.html' , adoptanimals=adoptanimals)


@app.route("/animaldetails/<int:adoptanimal_id>")
def animaldetails(adoptanimal_id):
    if 'user_id' not in session:
        return redirect('/loginpage')
    data = {
        'adoptanimal_id': adoptanimal_id
    }
    adoptanimal = Admin.get_adoptanimal_by_id(data)
    return render_template('animaldetails.html', adoptanimal=adoptanimal)
