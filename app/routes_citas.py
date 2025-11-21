from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Cita, Cliente, Mascota
from datetime import datetime, timedelta #Librerias para las fechas

appt = Blueprint("citas", __name__)

#Ruta para crear una nueva cita, enviando los datos del id del cliente y mascota, la fecha, motivo y duración, además se hace una sub consulta
#para obtener los clientes y mascotas registradas
@appt.route('/crear_cita', methods=['GET', 'POST'])
def crear_cita():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        mascota_id = request.form['mascota_id']
        fecha_hora = request.form['fecha_hora']
        motivo = request.form['motivo']
        duracion = request.form.get('duracion', 30)

        nueva_cita = Cita(
            cliente_id=cliente_id,
            mascota_id=mascota_id,
            fecha_hora=datetime.fromisoformat(fecha_hora),
            motivo=motivo,
            duracion=int(duracion),
            estado="pendiente"
        )

        db.session.add(nueva_cita)
        db.session.commit()

        flash("Cita registrada correctamente", "success")
        return redirect(url_for('citas.ver_citas'))

    clientes = Cliente.query.all()
    mascotas = Mascota.query.all()

    return render_template("citas/crear_cita.html", clientes=clientes, mascotas=mascotas)

#Esta ruta se utiliza para actualizar el estado de la cita desde el dashboard del 
# inicio del archivo index.html, a Pendiente, Confirmada,Cancelada o completada

@appt.route('/citas/<int:cita_id>/actualizar', methods=['POST'])
def actualizar_estado_cita(cita_id):
    cita = Cita.query.get_or_404(cita_id)

    nuevo_estado = request.form.get("estado")
    cita.estado = nuevo_estado

    db.session.commit()
    flash("Estado de la cita actualizado correctamente", "success")

    return redirect(url_for('citas.panel_citas'))
#Ruta para poder el listado completo de las citas, desde la plantilla lista_citas.html
@appt.route('/citas')
def ver_citas():
    citas = Cita.query.all()
    return render_template('citas/lista_citas.html', citas=citas)

#Ruta para acceder al home, y visualizar el dashboard principal, 
# además calcula las citas proximas y en curso, guardandolas en los arreglos[]

@appt.route('/home')
def panel_citas():
    now = datetime.now()
    citas = Cita.query.all()

    cita_en_curso = []
    citas_proximas = []
    finalizadas = []

    for cita in citas:
        inicio = cita.fecha_hora
        fin = cita.fecha_hora + timedelta(minutes=cita.duracion)

        if inicio <= now < fin:
            cita_en_curso.append(cita)
        elif now < inicio:
            citas_proximas.append(cita)
        else:
            finalizadas.append(cita)

    

    return render_template(
        'index.html',
        cita_en_curso=cita_en_curso,
        citas_proximas=citas_proximas,
        finalizadas=finalizadas
    )