from bson import ObjectId
from datetime import datetime
from src.database import Database

class Category:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def save(self):
        db = Database.get_db()
        result = db.categories.insert_one(self.to_dict())
        return str(result.inserted_id)
    
    @staticmethod
    def find_all():
        db = Database.get_db()
        categories = []
        for category in db.categories.find():
            category['_id'] = str(category['_id'])
            categories.append(category)
        return categories
    
    @staticmethod
    def find_by_id(category_id):
        db = Database.get_db()
        category = db.categories.find_one({'_id': ObjectId(category_id)})
        if category:
            category['_id'] = str(category['_id'])
        return category
    
    @staticmethod
    def find_by_name(name):
        db = Database.get_db()
        category = db.categories.find_one({'name': name})
        if category:
            category['_id'] = str(category['_id'])
        return category
    
    @staticmethod
    def update(category_id, data):
        db = Database.get_db()
        data['updated_at'] = datetime.utcnow()
        result = db.categories.update_one(
            {'_id': ObjectId(category_id)},
            {'$set': data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete(category_id):
        db = Database.get_db()
        result = db.categories.delete_one({'_id': ObjectId(category_id)})
        return result.deleted_count > 0

