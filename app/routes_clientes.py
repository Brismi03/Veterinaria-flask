from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Cliente

custom = Blueprint('clientes', __name__)


@custom.route("/clientes")
def listar_clientes():
    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)

    query = Cliente.query

    if search:
        query = query.filter(Cliente.nombre.ilike(f"%{search}%"))

    pagination = query.paginate(page=page, per_page=page_size)

    return render_template(
        "cliente.html",
        page_obj=pagination,
        search_query=search,
        page_size=page_size
    )

@custom.route("/clientes/crear", methods=["GET", "POST"])
def crear_cliente():
    if request.method == "POST":
        nombre = request.form["nombre"]
        edad = request.form.get("edad")
        direccion = request.form.get("direccion")
        telefono = request.form.get("telefono")
        email = request.form.get("email")

        nuevo = Cliente(
            nombre=nombre,
            edad=edad,
            direccion=direccion,
            telefono=telefono,
            email=email
        )

        db.session.add(nuevo)
        db.session.commit()

        flash("Cliente creado correctamente", "success")
        return redirect(url_for("clientes.listar_clientes"))

    return render_template("crear_cliente.html")
