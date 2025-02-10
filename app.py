# app.py
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from forms import RegistrationForm, LoginForm
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "abc123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db.init_app(app)

materias = [
    {
        "nombre": "Matematicas",
        "duracion": 90,
        "profesor": "Juan Perez",
        "dias": ["Lunes", "Miercoles"],
    },
    {
        "nombre": "Fisica",
        "duracion": 90,
        "profesor": "Julio Parra",
        "dias": ["Martes", "Jueves"],
    },
    {
        "nombre": "Quimica",
        "duracion": 90,
        "profesor": "Carlos Estrada",
        "dias": ["Lunes", "Viernes"],
    },
    {
        "nombre": "Geometria",
        "duracion": 90,
        "profesor": "Miguel Espinosa",
        "dias": ["Martes", "Miercoles"],
    },
    {
        "nombre": "Seminario",
        "duracion": 45,
        "profesor": "Andres Suarez",
        "dias": ["Jueves"],
    },
    {
        "nombre": "Ingles",
        "duracion": 90,
        "profesor": "Carla Suset",
        "dias": ["Jueves", "Viernes"],
    },
]

with app.app_context():
    db.create_all()


@app.route("/register", methods=["GET", "POST"])
def register():
    # Creamos una instancia del formulario de registro
    form = RegistrationForm()
    # Si el formulario se envía y es válido
    if form.validate_on_submit():
        # Verificamos si ya existe un usuario con la misma cédula de identidad
        existing_user = User.query.filter_by(id_card=form.id_card.data).first()
        # Si existe un usuario con la misma cédula de identidad
        if existing_user:
            flash("La cédula de identidad ya está registrada", "danger")
            return render_template("register.html", form=form)
        user = User(
            name=form.name.data,
            last_name=form.last_name.data,
            role=form.role.data,
            id_card=form.id_card.data,
            id_card_type=form.id_card_type.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        # Añadimos el usuario a la sesión de la base de datos
        db.session.add(user)
        # Guardamos los cambios en la base de datos
        db.session.commit()
        flash("Registro exitoso", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Creamos una instancia del formulario de inicio de sesión
    form = LoginForm()
    # Si el formulario se envía y es válido
    if form.validate_on_submit():
        user = User.query.filter_by(
            id_card=form.id_card.data,
            id_card_type=form.id_card_type.data,
            role=form.role.data,
        ).first()
        if user and user.check_password(form.password.data):
            session["user_id"] = user.id
            flash(f"Bienvenido, {user.name}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Inicio de sesión fallido, verifique sus credenciales", "danger")
    return render_template("login.html", form=form)


@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        user = User.query.filter_by(id=session["user_id"]).first()
        return render_template("dashboard.html", user=user)
    else:
        return redirect(url_for("login"))


@app.route("/horario", methods=["GET", "POST"])
def horario():
    if request.method == "POST":
        session["materias_seleccionadas"] = request.form.getlist("materias")
        return redirect(url_for("mostrar_horario"))
    return render_template("horario.html", materias=materias)


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))


@app.route("/")
def index():
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
