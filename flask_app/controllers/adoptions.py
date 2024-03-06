from flask_app import app
from flask import jsonify, render_template, redirect, session, request, flash, url_for
import paypalrestsdk
from flask_app.models.admin import Admin
from flask_app.models.adoption import Adoption
from flask_app.models.user import User
from flask_app.models.vet import Vet
from flask_app.models.package import Package
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import os   
from datetime import datetime
from werkzeug.utils import secure_filename


@app.route('/adoptpet/<int:adoptanimal_id>', methods=['GET', 'POST'])
def adopt_pet(adoptanimal_id):
    if 'user_id' not in session:
        return redirect('/loginpage')

    adoptanimal = Adoption.get_adoptanimal_by_id(adoptanimal_id)
    print(adoptanimal)
    if not adoptanimal:
        return render_template('404.html', message='Adopted animal not found')  # Handle case when adoptanimal is not found

    if request.method == 'GET':
        return render_template('adoptpetform.html', adoptanimal=adoptanimal)
    elif request.method == 'POST':
        if not Adoption.validate_adoption(request.form):
            return redirect(request.referrer)
        data = {
            "user_id": session['user_id'],
            "adoptanimal_id": adoptanimal_id,
            "reason": request.form['reason'],
            "adoption_date": request.form['adoption_date']
        }
        Adoption.create_adoption(data)
        return redirect('/dashboard')
    
    



 

 
    