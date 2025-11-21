from app import db
from datetime import datetime

#Modelo de la tabla cliente
class Cliente(db.Model):
    __tablename__ = 'clientes' #Nombre de la tabla
    #Atributos de la tabla 
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    edad = db.Column(db.Integer)
    direccion = db.Column(db.String(255))
    telefono = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True)

    mascotas = db.relationship('Mascota', back_populates='cliente', cascade='all, delete-orphan') #Relación con la tabla de mascota y eliminar en cascada
    citas = db.relationship('Cita', back_populates='cliente', cascade='all, delete-orphan') #Relación con la tabla citas y eliminar en casacada

    def __repr__(self):
        return f"<Cliente {self.id} {self.nombre}>"

#Modelo de la tabla mascota 
class Mascota(db.Model):
    __tablename__ = "mascotas" #Nombre de la tabla 
    #Atributos de la tabla 
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    especie = db.Column(db.String(20), nullable=False)
    raza = db.Column(db.String(50))
    edad = db.Column(db.Integer)
    peso = db.Column(db.Float)
    sexo = db.Column(db.String(1), nullable=False)
    esterilizado = db.Column(db.Boolean, default=True)

    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False) #Asignarle el id del cliente a la mascota

    imagen = db.Column(db.String(255))

    cliente = db.relationship("Cliente", back_populates="mascotas") #Relación con la tabla cliente
    citas = db.relationship("Cita", back_populates="mascota", cascade='all, delete-orphan') #Relación con la tabla mascota

    def __repr__(self):
        return f"<Mascota {self.nombre}>"

#modelo de la tabla citas
class Cita(db.Model):
    __tablename__ = 'citas' #Nombre de la tabla 
    #Atributos de la tabla
    id = db.Column(db.Integer, primary_key=True)

    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascotas.id'), nullable=False)

    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)
    motivo = db.Column(db.Text, nullable=False)
    duracion = db.Column(db.Integer, default=30)

    estado = db.Column(db.String(20), default='pendiente', nullable=False)

    cliente = db.relationship('Cliente', back_populates='citas')
    mascota = db.relationship('Mascota', back_populates='citas')

    def __repr__(self):
        return f"<Cita {self.id} - {self.mascota.nombre} ({self.cliente.nombre})>"
