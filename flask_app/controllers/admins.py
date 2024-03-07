import mailbox
import smtplib
from flask_app import app, socketio  # Import socketio from the main app module
from flask import render_template
from flask_socketio import SocketIO, send
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.admin import Admin
from flask_app.models.vet import Vet
from flask_app.models.adoption import Adoption
  
 



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
    if not Admin.validate_admin(data):
        return redirect('/loginadminpage')
    admin = Admin.get_admin_by_email(data)
    if not admin:
        flash('This email does not exist.', 'email')
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(admin['password'], request.form['password']):
        flash('Your password is wrong!', 'password')
        return redirect(request.referrer)
   
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
    adoptanimals = Admin.get_all_adoptanimals()
    return render_template('indexadmin.html', loggedAdmin=loggedAdmin, messages=messages, vets=vets, adoptanimals=adoptanimals)

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
    generated_password = Admin.generate_random_password()
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(generated_password),
        'specialization': request.form['specialization']
    }
    send_email_password(data['email'], generated_password)

    Vet.create_vet(data)
    return redirect('/dashboardadmin')

def send_email_password(email, password):
    LOGIN = ADMINEMAIL
    TOADDRS = email
    SENDER = ADMINEMAIL
    SUBJECT = 'INFO ABOUT YOUR ACCOUNT'
    
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
                % ((SENDER), "".join(TOADDRS), SUBJECT))
    msg += f"Dear User,\n\n"
    msg += f"Your account has been created. Your password is: {password}\n\nBest regards,\nPAWFECTION VET CLINIC"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(LOGIN, PASSWORD)
    server.sendmail(SENDER, TOADDRS, msg)
    server.quit()
    return redirect('/dashboardadmin')


@app.route("/adoptanimalsadmin")
def adoptanimalsadmin():
    if 'admin_id' not in session:
        return redirect('/loginadminpage')
    adoptanimals = Admin.get_all_adoptanimals()
    return render_template('adoptanimalsadmin.html', adoptanimals=adoptanimals )

@app.route("/adoptrequests/<int:adoptanimal_id>")
def adoptrequests(adoptanimal_id):
    if 'admin_id' not in session:
        return redirect('/loginadminpage')
    adoptanimalData = {
        "adoptanimal_id": adoptanimal_id
    }
    adoptanimal = Admin.get_adoptanimal_by_id(adoptanimalData)
    adoptrequests = Admin.get_adoptrequests(adoptanimalData)
    print(adoptrequests)
    return render_template('adoptrequests.html', adoptanimal=adoptanimal, adoptrequests=adoptrequests)


@app.route("/addanimal/new", methods=['POST'])
def newanimaladopt():
    if 'admin_id' not in session:
        return redirect('/loginadminpage')

    data={
        "name": request.form['name'],
        "specie": request.form['specie'],
        "description": request.form['description'],
        "picture": request.form['picture'],
        "age": request.form['age']
    }

    Admin.create_adopt_animal(data)
    return redirect('/adoptanimalsadmin')


@app.route("/addpost", methods=['POST'])
def addpost():
    if 'admin_id' not in session:
        return redirect('/loginadminpage')
    data = {
        "title": request.form['title'],
        "post": request.form['post'],
        "image": request.form['image'],
        "admin_id": session['admin_id']
    }
    Admin.create_post(data)
    return redirect('/dashboardadmin')

@app.route("/updatevetpage/<int:vet_id>")
def updatevet(vet_id):
    if 'admin_id' not in session:
        return redirect('/loginadminpage')
    vetData = {
        "vet_id": vet_id
    }
    vet = Vet.get_vet_by_id(vetData)
    return render_template('updatevet.html', vet=vet)

@app.route("/updatevet/<int:vet_id>", methods=['POST'])
def updatevetdata(vet_id):
    if 'admin_id' not in session:
        return redirect('/loginadminpage')
    data = {
        "vet_id": vet_id,
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "specialization": request.form['specialization']
    }
    Admin.update_vet(data)
    return redirect('/dashboardadmin')

# @app.route("/deletevet/<int:vet_id>")
# def deletevet(vet_id):
#     if 'admin_id' not in session:
#         return redirect('/loginadminpage')
#     vetData = {
#         "vet_id": vet_id
#     }
#     Admin.delete_animals_of_vet(vetData)
#     Admin.delete_appointments_of_vet(vetData)
#     Admin.delete_vet(vetData)

#     return redirect('/dashboardadmin')
from flask_mail import Mail, Message
# assuming you have initialized your Flask app and mail instance somewhere in your code

@app.route("/deletevet/<int:vet_id>")
def deletevet(vet_id):
    if 'admin_id' not in session:
        return redirect('/loginadminpage')

    vetData = {
        "vet_id": vet_id
    }

    # Get a list of users with accepted = 0 for the given vet
    pending_appointments = Admin.get_pending_appointments_for_vet(vetData)

    # Iterate over the list and send apology emails
    for appointment in pending_appointments:
        user_email = appointment['email']
        send_apology_email(user_email)

    # Delete animals, appointments, and vet
    Admin.delete_animals_of_vet(vetData)
    Admin.delete_appointments_of_vet(vetData)
    Admin.delete_vet(vetData)

    return redirect('/dashboardadmin')

def send_apology_email(user_email):
    LOGIN = ADMINEMAIL
    TOADDRS = user_email
    SENDER = ADMINEMAIL
    SUBJECT = 'INFO ABOUT APPOINTMENT'

    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
           % ((SENDER), "".join(TOADDRS), SUBJECT))
    msg += f"Dear User,\n\n We are very sorry but the vet you had an appointment isnt available anymore,please make another appointment with another vet.\n\nBest regards,\nPAWFECTION VET CLINIC"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(LOGIN, PASSWORD)
    server.sendmail(SENDER, TOADDRS, msg)
    server.quit()
    return redirect('/dashboardadmin')


     

@app.route("/acceptadoption/<int:adoptrequest_id>/<int:adoptanimal_id>")
def acceptadoption(adoptrequest_id, adoptanimal_id ):
    if 'admin_id' not in session:
        return redirect('/loginadminpage')
 
    addoption_details = Adoption.get_adoption_details(data={'adoption_id': adoptrequest_id})
    email = addoption_details['email']
    name = addoption_details['first_name']
    
    adoptionData = {
        "adoptrequest_id": adoptrequest_id,
        "adoptanimal_id": adoptanimal_id,
        "user_id": addoption_details['user_id']
    }

    Adoption.accept_adoption(adoptionData)
    # Adoption.change_status(adoptionData)
    Admin.delete_adoptions_of_adoptanimal(adoptionData)

    LOGIN = ADMINEMAIL
    TOADDRS = email
    SENDER = ADMINEMAIL
    SUBJECT = 'INFO ABOUT YOUR ADOPTION REQUEST'
    
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
                % ((SENDER), "".join(TOADDRS), SUBJECT))
    msg += f"Dear {name},\n\n"
    msg += f"We are pleased to inform you that your adoption request has been accepted. We are looking forward to welcoming you and your pet. If you have any questions or require further assistance, please do not hesitate to contact us.\n\nBest regards,\nPAWFECTION VET CLINIC"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(LOGIN, PASSWORD)
    server.sendmail(SENDER, TOADDRS, msg)
    server.quit()
    return redirect(request.referrer)

@app.route("/answer/<int:message_id>")
def answerpage(message_id):
    if 'admin_id' not in session:
        return redirect('/loginadminpage')
    messageData = {
        "message_id": message_id
    }
    message = Admin.get_message_by_id(messageData)
    return render_template('answer.html', message=message)


@app.route("/answer/<int:message_id>", methods=['POST'])
def answer(message_id):
    if 'admin_id' not in session:
        return redirect('/loginadminpage')
    message_id = message_id
    answer= request.form['answer']
    email= request.form['email']
    # data = {
    #     "message_id": message_id,
    #     "answer": request.form['answer']
    # }
    # Admin.answer_message(data)
    LOGIN = ADMINEMAIL
    TOADDRS = email
    SENDER = ADMINEMAIL
    SUBJECT = 'INFO ABOUT YOUR ADOPTION REQUEST'
    
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
                % ((SENDER), "".join(TOADDRS), SUBJECT))
    msg += f"Dear User,\n\n"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(LOGIN, PASSWORD)
    server.sendmail(SENDER, TOADDRS, msg)
    server.quit()
    return redirect('/dashboardadmin')




 




