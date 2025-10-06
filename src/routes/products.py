from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.models.product import Product
from bson.objectid import ObjectId
import html

products_bp = Blueprint('products', __name__)
@products_bp.route('/products', methods=['POST'])
def get_products():
    try:
        category_id = request.args.get('category')
        search = request.args.get('search')
        
        if search:
            products = Product.search(search)
        elif category_id:
            products = Product.find_by_category(category_id)
        else:
            products = Product.find_all()
        
        return jsonify({'success': True, 'products': products}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@products_bp.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.find_by_id(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Produto não encontrado'}), 404
        
        return jsonify({'success': True, 'product': product}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@products_bp.route("/products", methods=["POST"])
@jwt_required()
def create_product():
    try:
        data = request.get_json()
        
        required_fields = ['name', 'description', 'price', 'category_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'message': f'Campo {field} é obrigatório'}), 400
        
        # Validação e sanitização
        name = html.escape(data["name"]).strip()
        description = html.escape(data["description"]).strip()
        
        try:
            price = float(data["price"])
            if price <= 0:
                return jsonify({"success": False, "message": "Preço deve ser um valor positivo"}), 400
        except ValueError:
            return jsonify({"success": False, "message": "Preço deve ser um número válido"}), 400

        category_id = data["category_id"]
        if not ObjectId.is_valid(category_id):
            return jsonify({"success": False, "message": "ID de categoria inválido"}), 400

        images = [html.escape(img).strip() for img in data.get("images", [])]
        
        try:
            stock = int(data.get("stock", 0))
            if stock < 0:
                return jsonify({"success": False, "message": "Estoque não pode ser negativo"}), 400
        except ValueError:
            return jsonify({"success": False, "message": "Estoque deve ser um número inteiro válido"}), 400

        available = bool(data.get("available", True))

        product = Product(
            name=name,
            description=description,
            price=price,
            category_id=category_id,
            images=images,
            stock=stock,
            available=available
        )

        
        product_id = product.save()
        return jsonify({'success': True, 'product_id': product_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@products_bp.route('/products/<product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    try:
        data = request.get_json()
        
        # Validação e sanitização para update
        updated_data = {}
        if "name" in data: updated_data["name"] = html.escape(data["name"]).strip()
        if "description" in data: updated_data["description"] = html.escape(data["description"]).strip()
        
        if "price" in data:
            try:
                price = float(data["price"])
                if price <= 0:
                    return jsonify({"success": False, "message": "Preço deve ser um valor positivo"}), 400
                updated_data["price"] = price
            except ValueError:
                return jsonify({"success": False, "message": "Preço deve ser um número válido"}), 400

        if "category_id" in data:
            category_id = data["category_id"]
            if not ObjectId.is_valid(category_id):
                return jsonify({"success": False, "message": "ID de categoria inválido"}), 400
            updated_data["category_id"] = category_id

        if "images" in data:
            updated_data["images"] = [html.escape(img).strip() for img in data["images"]]
        
        if "stock" in data:
            try:
                stock = int(data["stock"])
                if stock < 0:
                    return jsonify({"success": False, "message": "Estoque não pode ser negativo"}), 400
                updated_data["stock"] = stock
            except ValueError:
                return jsonify({"success": False, "message": "Estoque deve ser um número inteiro válido"}), 400

        if "available" in data: updated_data["available"] = bool(data["available"])

        if Product.update(product_id, updated_data):
            return jsonify({"success": True, "message": "Produto atualizado com sucesso"}), 200
        else:
            return jsonify({"success": False, "message": "Produto não encontrado"}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@products_bp.route('/products/<product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    try:
        if Product.delete(product_id):
            return jsonify({'success': True, 'message': 'Produto excluído com sucesso'}), 200
        else:
            return jsonify({'success': False, 'message': 'Produto não encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

