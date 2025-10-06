from src.database import Database
from src.models.product import Product
from src.models.category import Category
from bson.objectid import ObjectId

Database.initialize()
db = Database.get_db()

def add_sample_products():
    # Adicionar categorias de exemplo
    category_names = ["Eletrônicos", "Roupas", "Livros", "Casa", "Esportes"]
    category_ids = {}
    for name in category_names:
        existing_category = Category.find_by_name(name)
        if not existing_category:
            category = Category(name=name, description=f"Produtos da categoria {name}")
            category_id = category.save()
            category_ids[name] = category_id
            print(f"Categoria {name} adicionada com ID: {category_id}")
        else:
            category_ids[name] = str(existing_category["_id"])
            print("Categoria " + name + " já existe com ID: " + str(existing_category["_id"]))

    # Adicionar produtos de exemplo
    products_data = [
        {
            "name": "Smartphone X",
            "description": "Smartphone de última geração com câmera de alta resolução.",
            "price": 2500.00,
            "category_id": category_ids["Eletrônicos"],
            "images": ["https://via.placeholder.com/150/0000FF/FFFFFF?text=SmartphoneX"],
            "stock": 50,
            "available": True
        },
        {
            "name": "Camiseta Algodão Pima",
            "description": "Camiseta super macia e confortável, 100% algodão Pima.",
            "price": 89.90,
            "category_id": category_ids["Roupas"],
            "images": ["https://via.placeholder.com/150/FF0000/FFFFFF?text=Camiseta"],
            "stock": 200,
            "available": True
        },
        {
            "name": "O Senhor dos Anéis",
            "description": "Clássico da literatura fantástica, edição de colecionador.",
            "price": 120.00,
            "category_id": category_ids["Livros"],
            "images": ["https://via.placeholder.com/150/00FF00/FFFFFF?text=Livro"],
            "stock": 100,
            "available": True
        },
        {
            "name": "Cafeteira Expresso",
            "description": "Cafeteira automática para um café perfeito a qualquer hora.",
            "price": 750.00,
            "category_id": category_ids["Casa"],
            "images": ["https://via.placeholder.com/150/FFFF00/000000?text=Cafeteira"],
            "stock": 30,
            "available": True
        },
        {
            "name": "Tênis de Corrida Pro",
            "description": "Tênis leve e responsivo para alta performance em corridas.",
            "price": 499.99,
            "category_id": category_ids["Esportes"],
            "images": ["https://via.placeholder.com/150/00FFFF/000000?text=Tenis"],
            "stock": 75,
            "available": True
        }
    ]

    for product_data in products_data:
        existing_product = db.products.find_one({"name": product_data["name"]})
        if not existing_product:
            product = Product(
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                category_id=product_data["category_id"],
                images=product_data["images"],
                stock=product_data["stock"],
                available=product_data["available"]
            )
            product_id = product.save()
            print("Produto " + product_data["name"] + " adicionado com ID: " + str(product_id))
        else:
            print("Produto " + product_data["name"] + " já existe.")

if __name__ == "__main__":
    add_sample_products()


