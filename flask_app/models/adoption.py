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
        query = "INSERT INTO adoptions (reason, adoption_date, user_id, adoptanimal_id ) VALUES (%(reason)s,%(adoption_date)s,%(user_id)s,%(adoptanimal_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    

    @classmethod
    def get_adoptanimal_by_id(cls, data):
        query = "SELECT * FROM adoptanimals WHERE id = %(adoptanimal_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
