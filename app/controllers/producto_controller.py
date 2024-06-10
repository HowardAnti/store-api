from flask import Blueprint, jsonify, request

from app.models.producto_model import Producto
from app.utils.decorators import jwt_required, roles_required
from app.views.producto_view import render_product_detail, render_product_list


producto_bp = Blueprint("producto", __name__)



@producto_bp.route("/products", methods=["GET"])
@jwt_required
@roles_required(["admin", "user"])
def get_productos():
    productos = Producto.get_all()
    return jsonify(render_product_list(productos))



@producto_bp.route("/products/<int:id>", methods=["GET"])
@jwt_required
@roles_required(["admin", "user"])
def get_producto(id):
    producto = Producto.get_by_id(id)
    if producto:
        return jsonify(render_product_detail(producto))
    return jsonify({"error": "Producto no encontrado"}),404



@producto_bp.route("/products", methods=["POST"])
@jwt_required
@roles_required(["admin"])
def create_productol():
    data = request.json
    name=data.get("name")
    description=data.get("description")
    price=data.get("price")
    stock=data.get("stock")

    if not name or not description or price is None or stock is None:
        return jsonify({"error": "Faltan datos requeridos"}), 400


    producto=Producto(name,description, price,stock)
    producto.save()

    return jsonify(render_product_detail(producto)), 201



@producto_bp.route("/products/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(["admin"])
def update_producto(id):
    producto = Producto.get_by_id(id)

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    data = request.json
    name=data.get("name")
    description=data.get("description")
    price=data.get("price")
    stock=data.get("stock")
    
    producto.update(name,description,price,stock)

    return jsonify(render_product_detail(producto))



@producto_bp.route("/products/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(["admin"])
def delete_producto(id):
    producto=Producto.get_by_id(id)
    if not producto:
        return jsonify({"error":"Producto no encontrado"}), 404
    
    producto.delete()
    return "", 204

