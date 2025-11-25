from database import db
from datetime import datetime

class Comentario(db.Model):
    __tablename__ = "comentario"

    id = db.Column(db.Integer, primary_key=True)
    autora = db.Column(db.String(120), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    poema_id = db.Column(db.Integer, db.ForeignKey("poema.id"), nullable=False)
