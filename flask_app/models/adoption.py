from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class Adoption():
    db_name = 'pawfection'
    def __init__(self, data):
        self.reason = data['reason']
        self.registation_date = data['registation_date']
        

    @classmethod
    def create_adoption(cls, data):
        query = "INSERT INTO adoptions (reason, adoption_date, user_id, adoptanimal_id,status) VALUES (%(reason)s,%(adoption_date)s,%(user_id)s,%(adoptanimal_id)s,0);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    

    @classmethod
    def get_adoptanimal_by_id(cls, adoptanimal_id):
        data = {"adoptanimal_id": adoptanimal_id}
        query = "SELECT * FROM adoptanimals WHERE id = %(adoptanimal_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return None
    
    @classmethod
    def get_adoptions_for_adoptanimal(cls, data):
        query = "SELECT * FROM adoptions WHERE adoptanimal_id = %(adoptanimal_id)s left join users on adoptions.user_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        adoptions = []
        if results:
            for adoption in results:
                adoptions.append(adoption)
            return adoptions
        return adoptions
    
    @classmethod
    def accept_adoption(cls, data):
        query = "UPDATE adoptanimals SET adopted=1 WHERE id = %(adoptanimal_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_adoption_details(cls, data):
        query = "SELECT adoptions.*, users.* FROM adoptions LEFT JOIN users ON adoptions.user_id = users.id WHERE adoptions.id = %(adoption_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def change_status(cls, data):
        query = "UPDATE adoptions SET status = 1 WHERE id = %(adoptanimal_id)s AND user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_adoptions_for_user(cls, data):
        query = "SELECT * FROM adoptions WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        adoptions = []
        if results:
            for adoption in results:
                adoptions.append(adoption)
            return adoptions
        return adoptions
    
    @staticmethod
    def validate_adoption(data):
        is_valid = True
        max_paragraph_length = 500  # Adjust the maximum length as needed
        if len(data['reason']) > max_paragraph_length:
            flash(f"Reason must not exceed {max_paragraph_length} characters., 'reason'")
            is_valid = False
        if len(data['adoption_date']) < 1:
            flash("Please enter a date.")
            is_valid = False
        return is_valid
    
 

