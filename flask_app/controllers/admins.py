from flask_app import app, socketio  # Import socketio from the main app module
from flask import render_template
from flask_socketio import SocketIO, send
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.admin import Admin
from flask_app.models.vet import Vet
  
 



UPLOAD_FOLDER = '/flask_app/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ADMINEMAIL = 'inatusha1@gmail.com'
PASSWORD = "godcnjwbemlgkotp"


######CHAT###################################################################################
socketio = SocketIO(app, cors_allowed_origins="*")
@socketio.on("message")
def sendMessage(message):
    send(message, broadcast=True)

@app.route("/chat")
def chat():
    return render_template("chat.html")
################################################################################################




@app.route('/loginadminpage')
def loginadminpage():
    if 'admin_id' in session:
        return redirect('/dashboardadmin') 
    return render_template('loginadmin.html')

@app.route('/loginadmin', methods=['POST'])
def loginadmin():
    data = {
        "email": request.form['email'],
        "password": request.form['password']
    }
    admin = Admin.get_admin_by_email(data)
    if not admin:
        flash("Invalid Email/Password")
        return redirect('/loginadminpage')
    if not bcrypt.check_password_hash(admin['password'], request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/loginadminpage')
    session['admin_id'] = admin['id']
    return redirect('/dashboardadmin')

@app.route('/dashboardadmin')
def dashboardadmin():
    if 'admin_id' not in session:
        return redirect('/loginadminpage')
    loggedAdminData = {
        'admin_id': session['admin_id']
    } 
    loggedAdmin = Admin.get_admin_by_id(loggedAdminData)
    if not loggedAdmin:
        return redirect('/logoutadmin')
    messages=Admin.get_all_messages()
    vets=Vet.get_all_vets()
    return render_template('indexadmin.html', loggedAdmin=loggedAdmin, messages=messages, vets=vets)

@app.route('/logoutadmin')
def logoutadmin():
    session.clear()
    return redirect('/loginadminpage')

@app.route('/messages')
def messages():
    if 'admin_id' not in session:
        return redirect('/loginadminpage')
    messages=Admin.get_all_messages()
    return render_template('messages.html', messages=messages)


@app.route("/addvet", methods=['POST'])
def addvet():
    if 'admin_id' not in session:
        return redirect('/loginadminpage')
    if Vet.get_vet_by_email(request.form):
        flash('This email already exists. Try another one.', 'emailSignUp')
        return redirect(request.referrer)
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'specialization': request.form['specialization']
    }
    Vet.create_vet(data)
    return redirect('/dashboardadmin')

@app.route("/adoptanimalsadmin")
def adoptanimalsadmin():
    if 'admin_id' not in session:
        return redirect('/loginadminpage')
    adoptanimals=Admin.get_all_adoptanimals()
    return render_template('adoptanimalsadmin.html', adoptanimals=adoptanimals)


@app.route("/addanimal/new", methods=['POST'])
def newanimaladopt():
    if 'admin_id' not in session:
        return redirect('/loginadminpage')

    data={
        "name": request.form['name'],
        "specie": request.form['specie'],
        "description": request.form['description'],
        "picture": request.form['picture']
    }

    Admin.create_adopt_animal(data)
    return redirect('/adoptanimalsadmin')
     




