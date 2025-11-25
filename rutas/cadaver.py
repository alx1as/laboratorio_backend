from flask import Blueprint, request, jsonify
from database import db
from modelos.cadaver import Cadaver
from modelos.cadaver_verso import CadaverVerso
from modelos.poema import Poema

from datetime import datetime

cadaver_bp = Blueprint("cadaver", __name__)

# ─────────────────────────────────────────────
# CREAR NUEVO
# ─────────────────────────────────────────────
@cadaver_bp.post("/cadaver/nuevo")
def crear_cadaver():
    data = request.get_json(force=True)

    nuevo = Cadaver(
        creado_por=data.get("creado_por", "Anónima"),
        fecha_creacion=datetime.utcnow().isoformat(),
        activo=True
    )

    db.session.add(nuevo)
    db.session.commit()

    return jsonify({"ok": True, "id": nuevo.id})

# ─────────────────────────────────────────────
# LISTAR TODOS LOS ABIERTOS
# ─────────────────────────────────────────────
@cadaver_bp.get("/cadaver/abiertos")
def abiertos():
    cadavers = Cadaver.query.filter_by(activo=True).order_by(Cadaver.id.desc()).all()

    respuesta = []
    for c in cadavers:
        respuesta.append({
            "id": c.id,
            "creado_por": c.creado_por,
            "fecha_creacion": c.fecha_creacion,
        })

    return jsonify(respuesta)

# ─────────────────────────────────────────────
# OBTENER UNO (incluye versos)
# ─────────────────────────────────────────────
@cadaver_bp.get("/cadaver/<int:id>")
def obtener(id):
    c = Cadaver.query.get(id)
    if not c:
        return jsonify(None)

    versos = [
        {"texto": v.texto, "autor": v.autor, "fecha": v.fecha}
        for v in c.versos
    ]

    return jsonify({
        "id": c.id,
        "creado_por": c.creado_por,
        "fecha_creacion": c.fecha_creacion,
        "activo": c.activo,
        "versos": versos
    })

# ─────────────────────────────────────────────
# AGREGAR VERSO
# ─────────────────────────────────────────────
@cadaver_bp.post("/cadaver/<int:id>/agregar")
def agregar(id):
    c = Cadaver.query.get(id)
    if not c or not c.activo:
        return jsonify({"error": "No está activo"}), 400

    data = request.get_json(force=True)

    nuevo = CadaverVerso(
        texto=data["texto"],
        autor=data.get("autor", "Anónima"),
        fecha=datetime.utcnow().isoformat(),
        cadaver_id=id
    )

    db.session.add(nuevo)
    db.session.commit()

    return jsonify({"ok": True})

# ─────────────────────────────────────────────
# FINALIZAR UN CADÁVER
# ─────────────────────────────────────────────
@cadaver_bp.post("/cadaver/<int:id>/finalizar")
def finalizar(id):
    c = Cadaver.query.get(id)
    if not c:
        return jsonify({"error": "No encontrado"}), 404

    # 1) Obtener versos
    versos = [v.texto for v in c.versos]

    # 2) Armar texto final del poema
    texto_final = "\n".join(versos)

    # 3) Crear Poema real
    nuevo_poema = Poema(
        autora=c.creado_por,
        etiqueta="Cadáver exquisito",
        texto=texto_final,
        imagen=None
    )

    db.session.add(nuevo_poema)

    # 4) Cerrar el cadáver
    c.activo = False

    db.session.commit()

    # 5) Devolver el poema recién creado
    return jsonify({
        "ok": True,
        "poema": {
            "id": nuevo_poema.id,
            "autora": nuevo_poema.autora,
            "etiqueta": nuevo_poema.etiqueta,
            "texto": nuevo_poema.texto,
            "fecha": nuevo_poema.fecha.isoformat() if nuevo_poema.fecha else None
        }
    })


# ─────────────────────────────────────────────
# LISTAR TODOS LOS FINALIZADOS
# ─────────────────────────────────────────────
@cadaver_bp.get("/cadaveres")
def cadaveres_finalizados():
    cadavers = Cadaver.query.filter_by(activo=False).order_by(Cadaver.id.desc()).all()

    resultado = []
    for c in cadavers:
        versos = [
            {"texto": v.texto, "autor": v.autor, "fecha": v.fecha}
            for v in c.versos
        ]

        resultado.append({
            "id": c.id,
            "creado_por": c.creado_por,
            "fecha_creacion": c.fecha_creacion,
            "versos": versos,
            "tipo": "cadaver"
        })

    return jsonify(resultado)
