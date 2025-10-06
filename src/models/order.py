from bson import ObjectId
from datetime import datetime
from src.database import Database

class Order:
    def __init__(self, customer_name, customer_phone, customer_address, items, total_amount, status="pending"):
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.customer_address = customer_address
        self.items = items  # Lista de dicionários com product_id, quantity, price
        self.total_amount = total_amount
        self.status = status  # pending, confirmed, shipped, delivered, cancelled
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'customer_address': self.customer_address,
            'items': self.items,
            'total_amount': self.total_amount,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def save(self):
        db = Database.get_db()
        result = db.orders.insert_one(self.to_dict())
        return str(result.inserted_id)
    
    @staticmethod
    def find_all():
        db = Database.get_db()
        orders = []
        for order in db.orders.find().sort('created_at', -1):
            order['_id'] = str(order['_id'])
            orders.append(order)
        return orders
    
    @staticmethod
    def find_by_id(order_id):
        db = Database.get_db()
        order = db.orders.find_one({'_id': ObjectId(order_id)})
        if order:
            order['_id'] = str(order['_id'])
        return order
    
    @staticmethod
    def update_status(order_id, status):
        db = Database.get_db()
        result = db.orders.update_one(
            {'_id': ObjectId(order_id)},
            {'$set': {'status': status, 'updated_at': datetime.utcnow()}}
        )
        return result.modified_count > 0
    
    @staticmethod
    def find_by_status(status):
        db = Database.get_db()
        orders = []
        for order in db.orders.find({'status': status}).sort('created_at', -1):
            order['_id'] = str(order['_id'])
            orders.append(order)
        return orders

