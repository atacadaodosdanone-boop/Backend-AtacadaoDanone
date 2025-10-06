from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.models.category import Category
from bson.objectid import ObjectId
import html

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = Category.find_all()
        return jsonify({'success': True, 'categories': categories}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@categories_bp.route('/categories/<category_id>', methods=['GET'])
def get_category(category_id):
    try:
        category = Category.find_by_id(category_id)
        if not category:
            return jsonify({'success': False, 'message': 'Categoria não encontrada'}), 404
        
        return jsonify({'success': True, 'category': category}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@categories_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    try:
        data = request.get_json()
        
        if 'name' not in data or not data['name'].strip():
            return jsonify({'success': False, 'message': 'Nome da categoria é obrigatório'}), 400
        
        name = html.escape(data['name']).strip()
        description = html.escape(data.get('description', '')).strip()

        # Verificar se já existe uma categoria com o mesmo nome
        existing_category = Category.find_by_name(name)
        if existing_category:
            return jsonify({'success': False, 'message': 'Categoria já existe'}), 400
        
        category = Category(
            name=name,
            description=description
        )

        
        category_id = category.save()
        return jsonify({'success': True, 'category_id': category_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@categories_bp.route('/categories/<category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    try:
        data = request.get_json()
        
        if Category.update(category_id, data):
            return jsonify({'success': True, 'message': 'Categoria atualizada com sucesso'}), 200
        else:
            return jsonify({'success': False, 'message': 'Categoria não encontrada'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@categories_bp.route('/categories/<category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    try:
        if Category.delete(category_id):
            return jsonify({'success': True, 'message': 'Categoria excluída com sucesso'}), 200
        else:
            return jsonify({'success': False, 'message': 'Categoria não encontrada'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

