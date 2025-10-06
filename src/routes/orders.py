from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.models.order import Order
from bson.objectid import ObjectId
import html
import re

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        
        required_fields = ['customer_name', 'customer_phone', 'customer_address', 'items', 'total_amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'message': f'Campo {field} é obrigatório'}), 400
        
        # Validar itens
        if not data['items'] or len(data['items']) == 0:
            return jsonify({'success': False, 'message': 'Pelo menos um item é obrigatório'}), 400
        
        # Validação e sanitização
        customer_name = html.escape(data["customer_name"]).strip()
        customer_phone = html.escape(data["customer_phone"]).strip()
        customer_address = html.escape(data["customer_address"]).strip()

        if not re.fullmatch(r"^\+?[0-9]{10,15}$", customer_phone):
            return jsonify({"success": False, "message": "Número de telefone inválido"}), 400

        items = []
        for item in data["items"]:
            if not all(k in item for k in ("product_id", "name", "quantity", "price")):
                return jsonify({"success": False, "message": "Item do pedido inválido"}), 400
            if not ObjectId.is_valid(item["product_id"]):
                return jsonify({"success": False, "message": "ID de produto inválido no item"}), 400
            try:
                quantity = int(item["quantity"])
                price = float(item["price"])
                if quantity <= 0 or price <= 0:
                    return jsonify({"success": False, "message": "Quantidade e preço do item devem ser positivos"}), 400
            except ValueError:
                return jsonify({"success": False, "message": "Quantidade ou preço do item inválido"}), 400
            items.append({
                "product_id": item["product_id"],
                "name": html.escape(item["name"]).strip(),
                "quantity": quantity,
                "price": price
            })

        try:
            total_amount = float(data["total_amount"])
            if total_amount <= 0:
                return jsonify({"success": False, "message": "Valor total deve ser positivo"}), 400
        except ValueError:
            return jsonify({"success": False, "message": "Valor total inválido"}), 400

        order = Order(
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_address=customer_address,
            items=items,
            total_amount=total_amount
        )

        
        order_id = order.save()
        return jsonify({'success': True, 'order_id': order_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@orders_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    try:
        status = request.args.get('status')
        
        if status:
            orders = Order.find_by_status(status)
        else:
            orders = Order.find_all()
        
        return jsonify({'success': True, 'orders': orders}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@orders_bp.route('/orders/<order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    try:
        order = Order.find_by_id(order_id)
        if not order:
            return jsonify({'success': False, 'message': 'Pedido não encontrado'}), 404
        
        return jsonify({'success': True, 'order': order}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@orders_bp.route('/orders/<order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    try:
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'success': False, 'message': 'Status é obrigatório'}), 400
        
        valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
        if data['status'] not in valid_statuses:
            return jsonify({'success': False, 'message': 'Status inválido'}), 400
        
        if Order.update_status(order_id, data['status']):
            return jsonify({'success': True, 'message': 'Status atualizado com sucesso'}), 200
        else:
            return jsonify({'success': False, 'message': 'Pedido não encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

