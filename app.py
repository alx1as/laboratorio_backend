from flask import Flask
from flask_cors import CORS
from config import Config
from database import db

# Crear la app primero
app = Flask(__name__)
app.config.from_object(Config)

CORS(app, supports_credentials=True)

# Inicializar DB
db.init_app(app)

# Importar modelos DESPUÉS de crear app y db
from modelos.poema import Poema
from modelos.comentario import Comentario
from modelos.cadaver import Cadaver


# Importar rutas DESPUÉS de modelos
from rutas.poemas import poemas_bp
from rutas.usuarios import usuarios_bp
from rutas.comentarios import comentarios_bp
from rutas.cadaver import cadaver_bp # NUEVA RUTA

# Registrar blueprints
app.register_blueprint(poemas_bp, url_prefix="/api")
app.register_blueprint(usuarios_bp, url_prefix="/api")
app.register_blueprint(comentarios_bp, url_prefix="/api")
app.register_blueprint(cadaver_bp, url_prefix="/api")  # NUEVO

# Crear tablas
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
