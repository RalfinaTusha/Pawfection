from flask_app.config.mysqlconnection import connectToMySQL
import re	 
from flask import flash


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User():
    db_name = 'pawfection'
    def __init__(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.animal= data['animal']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def get_animals_of_user(cls, data):
        query = "SELECT * FROM animals WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        animals = []
        if results:
            for animal in results:
                animals.append(animal)
            return animals
        return animals
    
    @classmethod
    def add_animal(cls, data):
        query = "INSERT INTO animals (name, species,age, user_id,vet_id) VALUES ( %(name)s, %(species)s, %(age)s,%(user_id)s,%(vet_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    

    @classmethod
    def get_all_users(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(cls.db_name).query_db(query)
        users= []
        if results:
            for user in results:
                users.append(user)
            return users
        return users

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT users.*, animals.* FROM users LEFT JOIN animals ON users.id = animals.user_id WHERE users.id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def edit_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email=%(email)s WHERE id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(user['first_name'])< 2:
            flash('First name must be more than 2 characters', 'firstName')
            is_valid = False
        if len(user['last_name'])< 2:
            flash('Last name must be more than 2 characters', 'lastName')
            is_valid = False
        if len(user['password'])< 8:
            flash('Password must be more or equal to 8 characters', 'password')
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash('The passwords do not match',  'confirmPassword')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_user_on_update(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(user['first_name'])< 2:
            flash('First name must be more than 2 characters', 'firstName')
            is_valid = False
        if len(user['last_name'])< 2:
            flash('Last name must be more than 2 characters', 'lastName')
            is_valid = False
        return is_valid
    
    @classmethod
    def update_profile_pic_user(cls, data):
        query = "UPDATE users SET profile_pic = %(image)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def add_appointment(cls, data):
        query = "INSERT INTO appointments (date, time,message,service, user_id, vet_id) VALUES (%(date)s, %(time)s,%(message)s,%(service)s, %(user_id)s, %(vet_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def send_message(cls, data):
        query = "INSERT INTO messages (subject, message, user_id,admin_id) VALUES (%(subject)s,%(message)s, %(user_id)s,%(admin_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_user_count(cls):
        query = "SELECT COUNT(*) as total FROM users;"
        result= connectToMySQL(cls.db_name).query_db(query)
        user=0
        if result:
            user=result[0]
            return user
        return user
    
    @classmethod
    def get_animal_count(cls):
        query = "SELECT COUNT(*) as total FROM animals;"
        result= connectToMySQL(cls.db_name).query_db(query)
        animal=0
        if result:
            animal=result[0]
            return animal
        return animal
    