from bson import ObjectId
from datetime import datetime
import hashlib
from src.database import Database

class Admin:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = self._hash_password(password)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def check_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest() == self.password_hash
    
    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def save(self):
        db = Database.get_db()
        result = db.admins.insert_one(self.to_dict())
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_username(username):
        db = Database.get_db()
        admin = db.admins.find_one({'username': username})
        if admin:
            admin['_id'] = str(admin['_id'])
        return admin
    
    @staticmethod
    def find_by_email(email):
        db = Database.get_db()
        admin = db.admins.find_one({'email': email})
        if admin:
            admin['_id'] = str(admin['_id'])
        return admin
    
    @staticmethod
    def find_by_id(admin_id):
        db = Database.get_db()
        admin = db.admins.find_one({'_id': ObjectId(admin_id)})
        if admin:
            admin['_id'] = str(admin['_id'])
        return admin
    
    @staticmethod
    def verify_password(stored_password_hash, provided_password):
        return hashlib.sha256(provided_password.encode('utf-8')).hexdigest() == stored_password_hash
    
    @staticmethod
    def create_default_admin():
        """Cria um administrador padrão se não existir nenhum"""
        db = Database.get_db()
        if db.admins.count_documents({}) == 0:
            admin = Admin('admin', 'admin@ecommerce.com', 'admin123')
            admin.save()
            return True
        return False

