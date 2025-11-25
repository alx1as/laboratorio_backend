from database import db
from datetime import datetime

class Poema(db.Model):
    __tablename__ = "poema"

    id = db.Column(db.Integer, primary_key=True)
    autora = db.Column(db.String, nullable=False)
    etiqueta = db.Column(db.String, nullable=False)
    fecha = db.Column(db.String, default=lambda: datetime.now().isoformat())
    texto = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.Text, nullable=True)

    comentarios = db.relationship(
        "Comentario",
        backref="poema",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "autora": self.autora,
            "etiqueta": self.etiqueta,
            "fecha": self.fecha,
            "texto": self.texto,
            "imagen": self.imagen,
            "comentarios": [
                {
                    "id": c.id,
                    "autora": c.autora,
                    "texto": c.texto,
                    "fecha": c.fecha.isoformat()
                }
                for c in self.comentarios
            ]
        }
