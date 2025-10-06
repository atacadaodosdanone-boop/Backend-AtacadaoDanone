from bson import ObjectId
from datetime import datetime
from src.database import Database

class Product:
    def __init__(self, name, description, price, category_id, images=None, stock=0, available=True):
        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id
        self.images = images or []
        self.stock = stock
        self.available = available
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category_id': self.category_id,
            'images': self.images,
            'stock': self.stock,
            'available': self.available,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def save(self):
        db = Database.get_db()
        result = db.products.insert_one(self.to_dict())
        return str(result.inserted_id)
    
    @staticmethod
    def find_all():
        db = Database.get_db()
        products = []
        for product in db.products.find():
            product['_id'] = str(product['_id'])
            products.append(product)
        return products
    
    @staticmethod
    def find_by_id(product_id):
        db = Database.get_db()
        product = db.products.find_one({'_id': ObjectId(product_id)})
        if product:
            product['_id'] = str(product['_id'])
        return product
    
    @staticmethod
    def find_by_category(category_id):
        db = Database.get_db()
        products = []
        for product in db.products.find({'category_id': category_id}):
            product['_id'] = str(product['_id'])
            products.append(product)
        return products
    
    @staticmethod
    def update(product_id, data):
        db = Database.get_db()
        data['updated_at'] = datetime.utcnow()
        result = db.products.update_one(
            {'_id': ObjectId(product_id)},
            {'$set': data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete(product_id):
        db = Database.get_db()
        result = db.products.delete_one({'_id': ObjectId(product_id)})
        return result.deleted_count > 0
    
    @staticmethod
    def search(query):
        db = Database.get_db()
        products = []
        search_filter = {
            '$or': [
                {'name': {'$regex': query, '$options': 'i'}},
                {'description': {'$regex': query, '$options': 'i'}}
            ]
        }
        for product in db.products.find(search_filter):
            product['_id'] = str(product['_id'])
            products.append(product)
        return products

