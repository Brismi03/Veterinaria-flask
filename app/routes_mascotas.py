from flask import Blueprint, render_template, request, redirect, url_for, flash,current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import Mascota, Cliente
import os

#Definir que extensiones se aceptan para la foto de la mascota
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

pet = Blueprint('mascotas', __name__)
#Ruta para crear una nueva mascota
@pet.route('/crear_mascota', methods=['GET','POST'])
def crear_mascota():
    if request.method == "POST": #Metodo post para enviar los datos de la mascota
        nombre = request.form["nombre"] 
        especie = request.form["especie"]
        raza = request.form.get("raza")
        edad = request.form.get("edad")
        peso = request.form.get("peso")
        sexo = request.form["sexo"]
        esterilizado = True if request.form.get("esterilizado") == "on" else False
        cliente_id = request.form["cliente_id"]

        imagen_file = request.files.get("imagen")
        nombre_imagen = None
        if imagen_file and allowed_file(imagen_file.filename): #Si se sube una imagen guardar en el archivo statics uploadas
            filename = secure_filename(imagen_file.filename)
            nombre_imagen = filename
            ruta = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            imagen_file.save(ruta)
        nueva_mascota = Mascota(
            nombre=nombre,
            especie=especie,
            raza=raza,
            edad=int(edad) if edad else None,
            peso=float(peso) if peso else None,
            sexo=sexo,
            esterilizado=esterilizado,
            cliente_id=cliente_id,
             imagen=nombre_imagen
        )

        db.session.add(nueva_mascota)
        db.session.commit() #Commit para guardar los datos en la BD

        flash("Mascota registrada correctamente", "success")
        return redirect(url_for("mascotas.listar_mascotas"))
    clientes = Cliente.query.all()
    return render_template("mascotas/crear_mascota.html", clientes=clientes) #Renderizar a la plantilla crear_mascota
#Ruta para ver todo el listado de mascotas
@pet.route("/lista")
def listar_mascotas():
    search_query = request.args.get("search", "") #Filtro para buscar 

    if search_query:
        mascotas = Mascota.query.join(Cliente).filter(
            db.or_(
                Mascota.nombre.ilike(f"%{search_query}%"), #Buscar por nombre de mascota
                Mascota.raza.ilike(f"%{search_query}%"), #Buscar por raza de la mascota 
                Cliente.nombre.ilike(f"%{search_query}%"),#Buscar también por nombre del cliente
            )
        ).all()
    else:
        mascotas = Mascota.query.all()

    return render_template(
        "mascotas/paciente.html",
        mascotas=mascotas,
        search_query=search_query
    )
#Ruta para ver el perfil de una mascota en especifico
@pet.route('/mascota/<int:mascota_id>') #Se pasa el atributo id
def ver_mascota(mascota_id):
    mascota = Mascota.query.get_or_404(mascota_id)
    return render_template('mascotas/perfil_mascota.html', mascota=mascota)