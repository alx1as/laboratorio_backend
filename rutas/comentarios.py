from flask import Blueprint, request, jsonify
from database import db
from modelos.comentario import Comentario

comentarios_bp = Blueprint("comentarios_bp", __name__)

@comentarios_bp.post("/poemas/<int:poema_id>/comentarios")
def crear_comentario(poema_id):
    data = request.json

    nuevo = Comentario(
        autora=data.get("autora", "Anónima"),
        texto=data.get("texto", ""),
        poema_id=poema_id
    )

    db.session.add(nuevo)
    db.session.commit()

    return jsonify({
        "id": nuevo.id,
        "autora": nuevo.autora,
        "texto": nuevo.texto,
        "fecha": nuevo.fecha.isoformat()
    })
