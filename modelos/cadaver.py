from database import db

class Cadaver(db.Model):
    __tablename__ = "cadaver"

    id = db.Column(db.Integer, primary_key=True)
    creado_por = db.Column(db.String, nullable=False)
    fecha_creacion = db.Column(db.String, nullable=False)
    activo = db.Column(db.Boolean, default=True)

    versos = db.relationship("CadaverVerso", backref="cadaver", lazy=True)
