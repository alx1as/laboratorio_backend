from flask import Blueprint, request, jsonify

usuarios_bp = Blueprint("usuarios_bp", __name__)

@usuarios_bp.post("/login")
def login():
    data = request.json
    nombre = data.get("nombre", "")
    return jsonify({"ok": True, "nombre": nombre})
