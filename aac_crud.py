from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to
        # access the MongoDB databases and collections.

        self.client = MongoClient('mongodb://%s:%s@localhost:27017' % (username, password))

        # ensure that the client opened properly
        if self.client is None:
            print('Failed')
        else:
            print('Success')

        self.database = self.client['aac']

    # adds the provided json values to the database
    def create(self, data):
        if data is not None:
            self.database.animals.insert_one(data)  # data should be dictionary
            return True
        else:
            return False

    # reads all of provided search term from the database and returns it
    def readAll(self, searchTerm):
        if searchTerm is not None:
            result = self.database.animals.find(searchTerm, {"_id": False})
            
            if result is not None:
                return result
                    
            else:
                raise Exception("Search value not found")
        else:
            raise Exception("Nothing to find, as the search term value is empty")
   
    # reads one of a provided search term from the database and returns it
    def read(self, searchTerm):
        if searchTerm is not None:
            result = self.database.animals.find(searchTerm, {"_id": False})
            if result is not None:    
                for data in result:
                    return data
                    
            else:
                raise Exception("Search value not found")
        else:
            raise Exception("Nothing to find, as the search term value is empty")
            
    # updates all documents in the database that are found with searchTerm using updateData
    def update(self, searchTerm, updateData):
        if searchTerm is not None:
            self.database.animals.find(searchTerm)
            if self.database.animals.find(searchTerm) is not None:
                for animal in self.database.animals.find(searchTerm):
                    self.database.animals.update_one(animal, {"$set": updateData}, upsert=False)
                
            else:
                raise Exception("Search value not found")
                
        else:
            raise Exception("Nothing to find, as the search term value is empty")
        
        return dumps(self.database.animals.find(searchTerm)) # returns json of the updated value
    
    # deletes all documents found using searchTerm
    def delete(self, searchTerm):
        if searchTerm is not None:
            animals = []
            if self.database.animals.find(searchTerm) is not None:
                for animal in self.database.animals.find(searchTerm):
                    self.database.animals.delete_one(animal)
                    animals.append(animal)
                
            else:
                raise Exception("Search value not found")
                
        else:
            raise Exception("Nothing to find, as the search term value is empty")
            
        return dumps(animals) # returns json of deleted value