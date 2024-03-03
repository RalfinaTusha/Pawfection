from flask_app.config.mysqlconnection import connectToMySQL
import re

class Admin():
    db_name = 'pawfection'
    def __init__(self, data):
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create_admin(cls, data):
        query = "INSERT INTO admins (email, password) VALUES (%(email)s,%(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_admin_by_email(cls, data):
        query = "SELECT * FROM admins WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def get_all_admins(cls):
        query = 'SELECT * FROM admins;'
        results = connectToMySQL(cls.db_name).query_db(query)
        admins= []
        if results:
            for admin in results:
                admins.append(admin)
            return admins
        return admins
    
    @classmethod
    def get_admin_by_id(cls, data):
        query = "SELECT * FROM admins WHERE id = %(admin_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    # @classmethod
    # def edit_admin(cls, data):
    #     query = "UPDATE admins SET first_name = %(first_name)s, last_name = %(last_name)s, email=%(email)s WHERE id = %(admin_id)s;"
    #     return connectToMySQL(cls.db_name).query_db(query, data)
    

    @classmethod
    def get_all_messages(cls):
        query = 'SELECT * FROM messages;'
        results = connectToMySQL(cls.db_name).query_db(query)
        messages= []
        if results:
            for message in results:
                messages.append(message)
            return messages
        return messages
    
    @classmethod
    def create_vet(cls, data):
        query = "INSERT INTO vets (first_name, last_name, email, password, specialization) VALUES ( %(first_name)s, %(last_name)s,%(email)s,%(password)s,%(specialization)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_all_adoptanimals(cls):
        query = 'SELECT * FROM adoptanimals WHERE adopted = 0;'
        results = connectToMySQL(cls.db_name).query_db(query)
        adoptanimals= []
        if results:
            for adoptanimal in results:
                adoptanimals.append(adoptanimal)
            return adoptanimals
        return adoptanimals
    
    @classmethod
    def get_adoptanimal_by_id(cls, data):
        query = "SELECT * FROM adoptanimals WHERE id = %(adoptanimal_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def create_adopt_animal(cls, data):
        query = "INSERT INTO adoptanimals ( name, specie, description, picture) VALUES (%(name)s,%(specie)s,%(description)s,%(picture)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)