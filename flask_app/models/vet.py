from flask_app.config.mysqlconnection import connectToMySQL
import re

class Vet():
    db_name = 'pawfection'
    def __init__(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.specialization = data['specialization']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_vet(cls, data):
        query = "INSERT INTO vets (first_name, last_name, email, password, specialization) VALUES ( %(first_name)s, %(last_name)s,%(email)s,%(password)s,%(specialization)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_vet_by_email(cls, data):
        query = "SELECT * FROM vets WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def get_all_vets(cls):
        query = 'SELECT * FROM vets;'
        results = connectToMySQL(cls.db_name).query_db(query)
        vets= []
        if results:
            for vet in results:
                vets.append(vet)
            return vets
        return vets
    
    @classmethod
    def get_vet_by_id(cls, data):
        query = "SELECT * FROM vets WHERE id = %(vet_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def edit_vet(cls, data):
        query = "UPDATE vets SET first_name = %(first_name)s, last_name = %(last_name)s, email=%(email)s WHERE id = %(vet_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def animals_by_vet(cls, data):
        query = "SELECT * FROM animals WHERE vet_id = %(vet_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        animals = []
        if results:
            for animal in results:
                animals.append(animal)
            return animals
        return animals
    
    @classmethod
    def update_profile_pic(cls, data):
        query = "UPDATE vets SET profile_pic = %(image)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    

    @classmethod
    def get_all_appointments(cls):
        query = 'SELECT * FROM appointments;'
        results = connectToMySQL(cls.db_name).query_db(query)
        appointments= []
        if results:
            for appointment in results:
                appointments.append(appointment)
            return appointments
        return appointments    

    @classmethod
    def get_appointment_by_id(cls, data):
        query = "SELECT * FROM appointments WHERE id = %(appointment_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def get_appointments_by_vet(cls, data):
        query = "SELECT * FROM appointments LEFT JOIN users ON appointments.user_id = users.id WHERE vet_id = %(vet_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        appointments = []
        if results:
            for appointment in results:
                appointments.append(appointment)
            return appointments
        return appointments
    
    @classmethod 
    def get_appointment_details(cls, data):
        query = "SELECT appointments.*, users.first_name AS user_first_name, users.last_name AS user_last_name, users.email AS user_email FROM appointments LEFT JOIN users ON appointments.user_id = users.id WHERE appointments.id = %(appointment_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def update_accept(cls, data):
        query = "UPDATE appointments SET accepted = 1 WHERE id = %(appointment_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def decline_accept(cls, data):
        query = "UPDATE appointments SET accepted = 2 WHERE id = %(appointment_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    

    @classmethod
    def get_vet_id_based_on_service(cls,service):
        service_vet_mapping = {
            "cat_sitting": 1,
            "dog_walk": 1,
            "pet_spa": 1,
            "pet_grooming": 2,
            "pet_daycare": 2,
        }

        if service in service_vet_mapping:
            return service_vet_mapping[service]
        else:
             return 3

    

