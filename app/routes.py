from flask import Blueprint, render_template

main = Blueprint('main', __name__)




@main.route('/lista-citas')
def lista_citas():
    return render_template('citas/lista_citas.html')

@main.route('/reportes')
def reportes():
    return render_template('reportes.html')


@main.route('/crear-cita')
def crear_cita():
    return render_template('citas/crear_cita.html')