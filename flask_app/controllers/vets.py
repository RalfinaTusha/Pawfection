from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app.models.admin import Admin
bcrypt = Bcrypt(app)
from flask_app.models.vet import Vet
  
import os   
from datetime import datetime
from werkzeug.utils import secure_filename
import smtplib

UPLOAD_FOLDER = '/flask_app/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ADMINEMAIL = 'inatusha1@gmail.com'
PASSWORD = "godcnjwbemlgkotp"

@app.route('/appointment/<int:appointment_id>', methods=['POST'])
def appointment(appointment_id):
    appointment_details = Vet.get_appointment_details(data={'appointment_id': appointment_id})
    accepeted = appointment_details['accepted']
    email=appointment_details['user_email']

    LOGIN = ADMINEMAIL
    TOADDRS = email
    SENDER = ADMINEMAIL
    SUBJECT = 'INFO ABOUT APPOINTMENT'
    
    if not appointment_details:
        return "Appointment not found", 404

    service = appointment_details['service']
    date = appointment_details['date']
    time = appointment_details['time']
    name=appointment_details['user_first_name']

    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
           % ((SENDER), "".join(TOADDRS), SUBJECT))

    if 'accept' in request.form:
        msg += f"Dear {name},\n\n"
        msg += f"Thank you for choosing our services.\n\nWe are pleased to inform you that your appointment for {service} on {date} at {time} has been accepted. We are looking forward to welcoming you and your pet. If you have any questions or require further assistance, please do not hesitate to contact us.\n\nBest regards,\nPAWFECTION VET CLINIC"
        Vet.update_accept(data={'appointment_id': appointment_id})

    elif 'decline' in request.form:
        msg += f"Dear {name},\n\n"
        msg += f"We regret to inform you that your appointment for {service} on {date} at {time} has been declined by the vet. \n\nWe apologize for any inconvenience this may have caused. If you have any concerns or would like to reschedule, please reach out to us. Thank you for your understanding.\n\nBest regards,\n PAWFECTION VET CLINIC"
        Vet.decline_accept(data={'appointment_id': appointment_id})

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(LOGIN, PASSWORD)
    server.sendmail(SENDER, TOADDRS, msg)
    server.quit()
    return redirect(request.referrer)

 
@app.route('/loginvetpage')
def loginVetPage():
    session.clear()
    if 'vet_id' in session:
        return redirect('/dashboardvet')
    return render_template('loginvet.html')

@app.route('/loginvet', methods=['POST'])
def loginvet():
    if 'vet_id' in session:
        return redirect('/dashboardvet')
    vet = Vet.get_vet_by_email(request.form)
    if not vet:
        flash('This email does not exist.', 'email')
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(vet['password'], request.form['password']):
        flash('Your password is wrong!', 'password')
        return redirect(request.referrer)
    session['vet_id'] = vet['id']
    return redirect('/dashboardvet')

@app.route('/dashboardvet')
def all_vets():
    if 'vet_id' not in session:
        return redirect('/loginvetpage')
    loggedVetData = {
        'vet_id': session['vet_id']
    } 
    loggedVet = Vet.get_vet_by_id(loggedVetData)
    animals=Vet.animals_by_vet(loggedVetData)
    appointments=Vet.get_appointments_by_vet(loggedVetData)
    three_posts=Admin.get_three_posts()
    if not loggedVet:
        return redirect('/logoutvet')
    return render_template('indexvet.html', loggedVet=loggedVet, animals=animals,appointments=appointments, three_posts=three_posts)

UPLOAD_FOLDER = 'flask_app/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.errorhandler(404) 
def invalid_route(e): 
    return render_template('404.html')


@app.route('/profilepic', methods=['POST'])
def new_profil_pic():
    if 'vet_id' not in session:
        return redirect('/loginvetpage')
    data = {"id": session['vet_id']}
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = secure_filename(image.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], current_time + filename)
            image.save(file_path)
            
            data["image"] = current_time + filename
            Vet.update_profile_pic(data)
    return redirect('/dashboardvet')


@app.route('/contactvetpage')
def contactvetpage():
    if 'vet_id' not in session:
        return redirect('/loginvetpage')
    three_posts=Admin.get_three_posts()
    return render_template('contactvet.html', three_posts=three_posts)

@app.route('/contactvet', methods=['POST'])
def contactvet():
    if 'vet_id' not in session:
        return redirect('/loginvetpage')

    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    LOGIN = ADMINEMAIL
    TOADDRS = email
    SENDER = ADMINEMAIL
    SUBJECT = subject

    msg = MIMEMultipart()
    msg.attach(MIMEText(message, 'plain', 'utf-8'))

    msg['From'] = SENDER
    msg['To'] = TOADDRS
    msg['Subject'] = SUBJECT

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(LOGIN, PASSWORD)
        server.sendmail(SENDER, TOADDRS, msg.as_string())
        server.quit()
    except Exception as e:
        # Handle the exception (print or log the error)
        print(f"Error: {e}")
        return "Error sending email"
    return redirect('/dashboardvet')
    

 




 
 


 



