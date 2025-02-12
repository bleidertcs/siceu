# Se importan las funciones y clases necesarias de Flask y otras librerías.
from flask import (
    Flask,
    render_template,
    redirect,
    request,
    url_for,
    session,
    flash,
)  # Funciones de Flask utilizadas para rutas, renderizar plantillas, redirecciones, manejo de sesiones y mensajes flash
from flask_sqlalchemy import (
    SQLAlchemy,
)  # Para configurar y utilizar SQLAlchemy con Flask
from models import (
    db,
    User,
)  # Se importan la instancia de la base de datos y el modelo User desde models.py
from forms import (
    RegistrationForm,
    LoginForm,
)  # Se importan los formularios de registro e inicio de sesión desde forms.py
from werkzeug.security import (
    check_password_hash,
)  # Para verificar contraseñas de forma segura

# Se crea una instancia de la aplicación Flask.
app = Flask(__name__)
# Se configura la clave secreta de la aplicación para la seguridad de las sesiones.
app.config["SECRET_KEY"] = "abc123"
# Se configura la URI de la base de datos a utilizar (en este caso, SQLite).
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
# Se inicializa la base de datos de SQLAlchemy con la aplicación configurada.
db.init_app(app)

# Se define una lista de materias disponibles con sus respectivos detalles.
materias = [
    {
        "nombre": "Matematicas",  # Nombre de la materia
        "hora": ["7:00 - 7:45 AM ", " 7:45 - 8:30 AM"],  # Duración en minutos
        "profesor": "Juan Perez",  # Nombre del profesor
        "dias": ["Lunes", "Miercoles"],  # Días en los que se dicta la materia
    },
    {
        "nombre": "Fisica",
        "hora": ["7:00 - 7:45 AM", "7:45 - 8:30 AM"],
        "profesor": "Julio Parra",
        "dias": ["Martes", "Jueves"],
    },
    {
        "nombre": "Quimica",
        "hora": ["8:30 - 9:15 AM ", " 9:15 - 10:00 AM"],
        "profesor": "Carlos Estrada",
        "dias": ["Lunes", "Viernes"],
    },
]

dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
horas = [
    "7:00 - 7:45 AM",
    "7:45 - 8:30 AM",
    "8:30 - 9:15 AM",
    "9:15 - 10:00 AM",
    "10:00 - 10:45 AM",
    "10:45 - 11:30 AM",
    "11:30 - 12:15 PM",
    "12:15 - 1:00 PM",
    "1:00 - 1:45 PM",
    "1:45 - 2:30 PM",
    "2:30 - 3:15 PM",
    "3:15 - 4:00 PM",
    "4:00 - 4:45 PM",
    "4:45 - 5:30 PM",  # Added more hours
]

# Se crea el esquema de la base de datos al entrar en el contexto de la aplicación.
with app.app_context():
    db.create_all()  # Crea todas las tablas definidas en los modelos si no existen


# Ruta para el registro de un nuevo usuario utilizando los métodos GET y POST.
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()  # Se crea una instancia del formulario de registro
    if (
        form.validate_on_submit()
    ):  # Se verifica si el formulario se envía y cumple con las validaciones
        # Se verifica si ya existe un usuario con la misma cédula de identidad en la base de datos
        existing_user = User.query.filter_by(id_card=form.id_card.data).first()
        if existing_user:  # Si se encuentra un usuario existente con la misma cédula
            flash(
                "La cédula de identidad ya está registrada", "danger"
            )  # Se muestra un mensaje de error
            return render_template(
                "register.html", form=form
            )  # Se vuelve a mostrar el formulario de registro
        # Si no existe el usuario, se crea una instancia del modelo User con los datos proporcionados
        user = User(
            name=form.name.data,  # Nombre del usuario
            last_name=form.last_name.data,  # Apellido del usuario
            role=form.role.data,  # Rol del usuario
            id_card=form.id_card.data,  # Cédula de identidad
            id_card_type=form.id_card_type.data,  # Tipo de cédula de identidad
            email=form.email.data,  # Correo electrónico
        )
        user.set_password(
            form.password.data
        )  # Se establece la contraseña del usuario de forma segura
        db.session.add(user)  # Se añade el usuario a la sesión de la base de datos
        db.session.commit()  # Se guardan los cambios en la base de datos
        flash(
            "Registro exitoso", "success"
        )  # Se muestra un mensaje de éxito al usuario
        return redirect(
            url_for("login")
        )  # Se redirige al usuario a la página de inicio de sesión
    return render_template(
        "register.html", form=form
    )  # Si el formulario no se envía o es inválido, se renderiza la plantilla de registro


# Ruta para el inicio de sesión utilizando los métodos GET y POST.
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()  # Se crea una instancia del formulario de inicio de sesión
    if form.validate_on_submit():  # Se verifica si el formulario se envía y es válido
        # Se busca en la base de datos el usuario que coincida con la cédula de identidad, el tipo de cédula y el rol proporcionados
        user = User.query.filter_by(
            id_card=form.id_card.data,
            id_card_type=form.id_card_type.data,
            role=form.role.data,
        ).first()
        # Si se encuentra el usuario y la contraseña es correcta
        if user and user.check_password(form.password.data):
            session["user_id"] = (
                user.id
            )  # Se guarda el id del usuario en la sesión para mantener lo autenticado
            flash(
                f"Bienvenido, {user.name}!", "success"
            )  # Se muestra un mensaje de bienvenida
            return redirect(
                url_for("dashboard")
            )  # Se redirige al usuario al panel de control
        else:
            flash(
                "Inicio de sesión fallido, verifique sus credenciales", "danger"
            )  # Mensaje de error si las credenciales son incorrectas
    return render_template(
        "login.html", form=form
    )  # Se renderiza la plantilla de inicio de sesión con el formulario


# Ruta para el panel de control (dashboard) que se muestra sólo si el usuario está autenticado.
@app.route("/dashboard")
def dashboard():
    if (
        "user_id" in session
    ):  # Se verifica si el usuario está autenticado (existe "user_id" en la sesión)
        user = User.query.get(
            session["user_id"]
        )  # Se obtiene el usuario de la base de datos usando el id almacenado en la sesión
        return render_template(
            "dashboard.html", user=user
        )  # Se renderiza la plantilla del dashboard pasando el usuario
    else:
        return redirect(
            url_for("login")
        )  # Si no está autenticado, se redirige a la página de inicio de sesión


# Ruta para gestionar el horario, admite métodos GET y POST.
@app.route("/horario", methods=["GET", "POST"])
def horario():
    if request.method == "POST":  # Si se envía el formulario mediante POST
        # Se almacenan en la sesión las materias seleccionadas enviadas desde el formulario (como una lista)
        session["materias_seleccionadas"] = request.form.getlist("materias")
        return redirect(
            url_for("mostrar_horario")
        )  # Se redirige a la ruta que mostrará el horario generado
    # Si el método es GET, se renderiza la plantilla de horario mostrando las materias disponibles
    return render_template("horario.html", materias=materias)


@app.route("/coordinador_horario", methods=["GET", "POST"])
def coordinador_horario():
    if "user_id" not in session or not session["user_id"]:
        return redirect(url_for("login"))  # Redirect if not logged in
    user = User.query.get(session["user_id"])
    if user.role != "coordinador":
        return redirect(url_for("dashboard"))  # Redirect if not coordinator

    if request.method == "POST":
        nombre_materia = request.form["nombre_materia"]
        nombre_profesor = request.form["nombre_profesor"]
        horas_clase = request.form.getlist("horas_clase")  # Get list of selected hours
        dias_seleccionados = request.form.getlist("dias_seleccionados")

        nueva_materia = {
            "nombre": nombre_materia,
            "hora": horas_clase,
            "profesor": nombre_profesor,
            "dias": dias_seleccionados,
        }
        materias.append(nueva_materia)  # Add to the materias list
        flash("Materia agregada correctamente.", "success")
        return redirect(url_for("coordinador_horario"))

    return render_template(
        "coordinador_horario.html",
        dias_semana=dias_semana,
        horas=horas,
        materias=materias,
    )


# Ruta para cerrar la sesión del usuario.
@app.route("/logout")
def logout():
    session.pop(
        "user_id", None
    )  # Se elimina "user_id" de la sesión para cerrar la sesión del usuario
    return redirect(
        url_for("login")
    )  # Se redirige al usuario a la página de inicio de sesión


# Ruta principal que redirige a la página de inicio de sesión.
@app.route("/")
def index():
    return redirect(
        url_for("login")
    )  # Redirige automáticamente a la ruta de inicio de sesión


# Punto de entrada principal de la aplicación.
if __name__ == "__main__":
    app.run(debug=True)  # Ejecuta la aplicación en modo de depuración
