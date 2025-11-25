from database import db

class CadaverVerso(db.Model):
    __tablename__ = "cadaver_verso"

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.String, nullable=False)
    autor = db.Column(db.String, nullable=False)

    cadaver_id = db.Column(db.Integer, db.ForeignKey("cadaver.id"), nullable=False)
