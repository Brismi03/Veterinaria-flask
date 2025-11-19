from app import create_app, db
from app.models import Cliente

app = create_app()

with app.app_context():
    db.create_all()

    # Datos de prueba opcionales
    c = Cliente(nombre="Juan Pérez",edad=31,direccion="Av.Tecnologico", telefono="55-5555", email="juan@gmail.com")
    db.session.add(c)
    db.session.commit()

    print("Base de datos creada y cliente agregado.")