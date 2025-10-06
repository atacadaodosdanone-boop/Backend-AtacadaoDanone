import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # MongoDB Configuration
    MONGO_URI = os.environ.get(\'MONGO_URI\') or \'mongodb+srv://atacadaodosdanone_db_user:PFZdVRSnsBm1Q5ZY@cluster0.lplaiox.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0\' 
    # CORS Configuration
    CORS_ORIGINS = ['*']  # Permitir qualquer origem em produção

