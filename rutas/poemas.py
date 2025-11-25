from flask import Blueprint, request, jsonify
from modelos.poema import Poema
from database import db

poemas_bp = Blueprint("poemas_bp", __name__)

# Aceptar /poemas y /poemas/
@poemas_bp.get("/poemas")
@poemas_bp.get("/poemas/")
def listar():
    poemas = Poema.query.order_by(Poema.id.desc()).all()
    return jsonify([p.to_dict() for p in poemas])

# Aceptar /poemas y /poemas/
@poemas_bp.post("/poemas")
@poemas_bp.post("/poemas/")
def crear():
    data = request.json

    nuevo = Poema(
        autora=data["autora"],
        etiqueta=data["etiqueta"],
        texto=data["texto"],
        imagen=data.get("imagen")
    )

    db.session.add(nuevo)
    db.session.commit()

    return jsonify(nuevo.to_dict())
