
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app 
from flask_app.models import user


class Adventure:
    db = "nb"
    def __init__(self,data):
        self.id = data['id']
        self.city= data['city']
        self.country = data['country']
        self.arrival = data['arrival']
        self.departure= data['departure']
        self.memories = data['memories']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None



    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM adventures
                JOIN users on adventures.user_id = users.id;
                """
        results = connectToMySQL(cls.db).query_db(query)
        adventures = []
        for row in results:
            this_adventure = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_adventure.creator = user.User(user_data)
            adventures.append(this_adventure)
        return adventures

    @classmethod
    def get_all_adventures_with_creator(cls,data):
        query = """ SELECT * FROM adventures 
        LEFT JOIN users ON adventures.user_id 
        WHERE users.id = %(id);"""
        result = connectToMySQL(cls.db).query_db(query,data)
        if not result:
            return False

        all_adventures = []
        
        one_adventure = cls(result)
        one_adventures_creator_info = {
                "id": result['users.id'], 
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at'],
            }
            
        creator = user.User(one_adventures_creator_info)
        one_adventure.creator = creator
        all_adventures.append(one_adventure)
        return all_adventures






    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM adventures
                JOIN users on adventures.user_id = users.id
                WHERE adventures.id = %(id)s;
                """
        result = connectToMySQL(cls.db).query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_adventure = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_adventure = user.User(user_data)
        return this_adventure
    



    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM adventures WHERE id = %(id)s" 
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        if len(results) < 1: 
            return False 
        return cls(results[0])



    @classmethod
    def save(cls,data):
        query = "INSERT INTO adventures (city, country, arrival, departure,memories,user_id) VALUES(%(city)s, %(country)s, %(arrival)s, %(departure)s,  %(memories)s, %(user_id)s);" 
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return results




    @classmethod
    def destory(cls, data):
        query = "DELETE FROM adventures WHERE id=%(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        return result



    @classmethod  
    def update(cls, data):
        query = "UPDATE adventures SET city = %(city)s, country = %(country)s, arrival = %(arrival)s, departure = %(departure)s WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return results

    @classmethod
    def get_year(cls):
        # query = """SELECT
        # EXTRACT(YEAR FROM arrival) AS year
        # FROM adventures;""" 
        query = """

    SELECT 
    YEAR(Arrival) AS ArrivalYear
    FROM Adventures;
        """
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        if len(results) < 1: 
            return False 
        return (results[0])


#### Static method ####
    @classmethod
    def is_valid_adventure(cls, adventure):
        is_valid = True

        if len(adventure["city"]) <= 2:
            flash("City must be at least 2 characters.")
            is_valid = False
            
        if len(adventure["country"]) <= 2:
            flash("Country must be at least 2 characters.")
            is_valid = False
        
        if len(adventure["arrival"]) <= 0:
            flash("arrival is required.")
            is_valid = False

        if len(adventure["departure"]) <= 0:
            flash("departure is required.")
            is_valid = False
            
        if len(adventure["memories"]) <= 10:
            flash(" memories must be more than 10 characters.")
            is_valid = False
        

        #test    
        print ("validation - adventure is valid", is_valid)
        return is_valid

