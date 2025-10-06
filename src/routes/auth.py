from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.admin import Admin

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if 'username' not in data or 'password' not in data:
            return jsonify({'success': False, 'message': 'Username e password são obrigatórios'}), 400
        
        admin = Admin.find_by_username(data['username'])
        if not admin:
            return jsonify({'success': False, 'message': 'Credenciais inválidas'}), 401
        
        if not Admin.verify_password(admin['password_hash'], data['password']):
            return jsonify({'success': False, 'message': 'Credenciais inválidas'}), 401
        
        access_token = create_access_token(identity=admin['_id'])
        return jsonify({
            'success': True,
            'access_token': access_token,
            'admin': {
                'id': admin['_id'],
                'username': admin['username'],
                'email': admin['email']
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'message': f'Campo {field} é obrigatório'}), 400
        
        # Verificar se já existe um admin com o mesmo username ou email
        existing_admin = Admin.find_by_username(data['username'])
        if existing_admin:
            return jsonify({'success': False, 'message': 'Username já existe'}), 400
        
        existing_admin = Admin.find_by_email(data['email'])
        if existing_admin:
            return jsonify({'success': False, 'message': 'Email já existe'}), 400
        
        admin = Admin(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        admin_id = admin.save()
        return jsonify({'success': True, 'admin_id': admin_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@auth_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_admin():
    try:
        admin_id = get_jwt_identity()
        admin = Admin.find_by_id(admin_id)
        
        if not admin:
            return jsonify({'success': False, 'message': 'Admin não encontrado'}), 404
        
        return jsonify({
            'success': True,
            'admin': {
                'id': admin['_id'],
                'username': admin['username'],
                'email': admin['email']
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

