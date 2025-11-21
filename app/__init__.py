import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    load_dotenv()

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Configurar la BD
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #Configuración para subir imagenes
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  


    # Inicializar SQLAlchemy
    db.init_app(app)

    # Registrar rutas 
    from .routes import main
    app.register_blueprint(main)

    from .routes_clientes import customer
    app.register_blueprint(customer)

    from .routes_mascotas import pet
    app.register_blueprint(pet)

    from .routes_citas import appt
    app.register_blueprint(appt)

    return app
