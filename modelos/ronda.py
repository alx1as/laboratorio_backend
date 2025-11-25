from database import db

class Ronda(db.Model):
    __tablename__ = "ronda"

    id = db.Column(db.Integer, primary_key=True)
    creada_por = db.Column(db.String, nullable=False)
    fecha_creacion = db.Column(db.String, nullable=False)
    activa = db.Column(db.Boolean, default=True)  # 🔥 NUEVA COLUMNA

    versos = db.relationship("CadaverPoema", backref="ronda", lazy=True)
