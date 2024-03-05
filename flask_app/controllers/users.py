from flask_app import app
from flask import jsonify, render_template, redirect, session, request, flash, url_for
import paypalrestsdk
from flask_app.models.admin import Admin
from flask_app.models.user import User
from flask_app.models.vet import Vet
from flask_app.models.package import Package
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
        'user_id': session['user_id'],
        
    } 
    loggedUser = User.get_user_by_id(loggedUserData)
    animals=User.get_animals_of_user(loggedUserData)
    user_count = User.get_user_count()
    animal_count = User.get_animal_count() 
    three_posts=Admin.get_three_posts()
    packages=Package.get_all_packages()
 

    if not loggedUser:
        return redirect('/logout')
    return render_template('index.html', loggedUser=loggedUser,animals=animals, user_count=user_count, three_posts=three_posts ,packages=packages, animal_count=animal_count)




 
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
        flash('This email does not exist.', 'email')
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash('Your password is wrong!', 'password')
        return redirect(request.referrer)
    session['user_id'] = user['id']
    return redirect('/')

@app.route('/contact')
def contact():
    if 'user_id' not in session:
        return redirect('/')
    three_posts=Admin.get_three_posts()

    return render_template('contact.html', three_posts=three_posts)

@app.route('/services')
def services():
    if 'user_id' not in session:
        return redirect('/')
    three_posts=Admin.get_three_posts()
    return render_template('services.html', three_posts=three_posts)


@app.route('/prices')
def prices():
    if 'user_id' not in session:
        return redirect('/')
    three_posts=Admin.get_three_posts()
    return render_template('pricing.html', three_posts=three_posts)


@app.route('/vets')
def vets():
    if 'user_id' not in session:
        return redirect('/')
    vets= Vet.get_all_vets()
    three_posts=Admin.get_three_posts()
    return render_template('vet.html',vets=vets, three_posts=three_posts)

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
    three_posts=Admin.get_three_posts()
    return render_template('profile.html', user = user, animals = animals, vets = vets, three_posts=three_posts)


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

UPLOAD_FOLDER = 'flask_app/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    three_posts=Admin.get_three_posts()

    return render_template('adoptanimals.html' , adoptanimals=adoptanimals, three_posts=three_posts)


@app.route("/animaldetails/<int:adoptanimal_id>")
def animaldetails(adoptanimal_id):
    if 'user_id' not in session:
        return redirect('/loginpage')
    data = {
        'adoptanimal_id': adoptanimal_id
    }
    adoptanimal = Admin.get_adoptanimal_by_id(data)
    three_posts=Admin.get_three_posts()

    return render_template('animaldetails.html', adoptanimal=adoptanimal, three_posts=three_posts)


@app.route("/blogpage")
def blogpage():
    if 'user_id' not in session:
        return redirect('/')
    posts=Admin.get_all_posts()
    three_posts=Admin.get_three_posts()

    return render_template('blog.html', posts=posts, three_posts=three_posts)
     

@app.route("/post/new/<int:post_id>")
def newpost(post_id):
    if 'user_id' not in session:
        return redirect('/loginadminpage')
    data = {
        'post_id': post_id
    }
    post = Admin.get_post_by_id(data)
    three_posts=Admin.get_three_posts()
    return render_template('singlepost.html', post=post, three_posts=three_posts)


@app.route('/checkout/paypal/<int:id>')
def checkoutPaypal(id):
    if 'user_id' not in session:
            return redirect('/')
    
    data = {
        'id': id
    }
    package = Package.get_package_by_id(data)
    
    totalPrice = package['price']

    try:
        paypalrestsdk.configure({
            "mode": "sandbox", # Change this to "live" when you're ready to go live
            "client_id": "AYckYn5asNG7rR9A2gycCw-N2Du3GXH4ytNfU5ueLeYKaUwjKFL-aZMu3owCwfs_D1fydp2W-HSVieZ0",
            "client_secret": "EJu8H94UNn6b2Xigp26rf1pIs6NW-WrweGw-RkboWLUjWfHK2m46qrFObh_rL_HPSwvfipNyFoYdoa3K"
        })

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": totalPrice,
                    "currency": "USD"  # Adjust based on your currency
                },
                "description": f"Pagese per parkim per makinen me targe orë!"
            }],
            "redirect_urls": {
                "return_url": url_for('paymentSuccess', _external=True, totalPrice=totalPrice,package_id=id),
                "cancel_url": "http://example.com/cancel"
            }
        })

        if payment.create():
            approval_url = next(link.href for link in payment.links if link.rel == 'approval_url')
            return redirect(approval_url)
        else:
            flash('Something went wrong with your payment', 'creditCardDetails')
            return redirect(request.referrer)
    except paypalrestsdk.ResourceNotFound as e:
        flash('Something went wrong with your payment', 'creditCardDetails')
        return redirect(request.referrer)






@app.route("/success", methods=["GET"])
def paymentSuccess():
    payment_id = request.args.get('paymentId', '')
    payer_id = request.args.get('PayerID', '')
    try:
        paypalrestsdk.configure({
            "mode": "sandbox", # Change this to "live" when you're ready to go live
            "client_id": "AYckYn5asNG7rR9A2gycCw-N2Du3GXH4ytNfU5ueLeYKaUwjKFL-aZMu3owCwfs_D1fydp2W-HSVieZ0",
            "client_secret": "EJu8H94UNn6b2Xigp26rf1pIs6NW-WrweGw-RkboWLUjWfHK2m46qrFObh_rL_HPSwvfipNyFoYdoa3K"
        })
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            
            print("////////////////////////////////////////////////////")
            
            ammount = request.args.get('totalPrice')
            status = 'Paid'
            user_id = session['user_id']
            package_id = request.args.get('package_id')
            data = {
                'ammount': ammount,
                'status': status,
                'user_id': user_id,
                'package_id': package_id,
            }
            Package.createPayment(data)
           
            flash('Your payment was successful!', 'paymentSuccessful')
            return redirect('/dashboard')
        else:
            print("")
            flash('Something went wrong with your payment', 'paymentNotSuccessful')
            return redirect('/')
    except paypalrestsdk.ResourceNotFound as e:
        flash('Something went wrong with your payment', 'paymentNotSuccessful')
        return redirect('/dashboard')


@app.route("/cancel", methods=["GET"])
def paymentCancel():
    flash('Payment was canceled', 'paymentCanceled')
    return redirect('/dashboard')