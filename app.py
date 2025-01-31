# app.py
# Importamos las librerías necesarias
from flask import Flask, render_template, redirect, url_for, session, flash # Flask para el framework web, render_template para renderizar plantillas HTML, redirect y url_for para manejar redirecciones, session para manejar sesiones de usuario, flash para mostrar mensajes al usuario
from flask_sqlalchemy import SQLAlchemy # SQLAlchemy para interactuar con la base de datos
from models import db, User # Importamos la base de datos y el modelo User desde models.py
from forms import RegistrationForm, LoginForm # Importamos los formularios de registro y login desde forms.py
from werkzeug.security import check_password_hash # Función para verificar contraseñas hash

# Creamos una instancia de la aplicación Flask
app = Flask(__name__)

# Configuraciones de la aplicación
app.config['SECRET_KEY'] = 'abc123' # Clave secreta para firmar las cookies de sesión
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # URL de la base de datos SQLite
db.init_app(app) # Inicializamos la base de datos con la aplicación Flask

# Creamos las tablas de la base de datos si no existen
with app.app_context():
    db.create_all()

# Ruta para el registro de usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Creamos una instancia del formulario de registro
    form = RegistrationForm()
    # Si el formulario se envía y es válido
    if form.validate_on_submit():
        # Verificamos si ya existe un usuario con la misma cédula de identidad
        existing_user = User.query.filter_by(id_card=form.id_card.data).first()
        # Si existe un usuario con la misma cédula de identidad
        if existing_user:
            # Mostramos un mensaje de error
            flash('La cédula de identidad ya está registrada', 'danger')
            # Renderizamos la plantilla de registro con el formulario y el mensaje de error
            return render_template('register.html', form=form)
        # Si no existe un usuario con la misma cédula de identidad
        # Creamos un nuevo usuario con los datos del formulario
        user = User(name=form.name.data,
                    last_name=form.last_name.data,
                    role=form.role.data,
                    id_card=form.id_card.data,
                    id_card_type=form.id_card_type.data,
                    email=form.email.data)
        # Establecemos la contraseña del usuario utilizando la función set_password del modelo User
        user.set_password(form.password.data)
        # Añadimos el usuario a la sesión de la base de datos
        db.session.add(user)
        # Guardamos los cambios en la base de datos
        db.session.commit()
        # Mostramos un mensaje de éxito
        flash('Registro exitoso', 'success')
        # Redirigimos al usuario a la página de inicio de sesión
        return redirect(url_for('login'))
    # Si el formulario no se ha enviado o no es válido, renderizamos la plantilla de registro con el formulario
    return render_template('register.html', form=form)

# Ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Creamos una instancia del formulario de inicio de sesión
    form = LoginForm()
    # Si el formulario se envía y es válido
    if form.validate_on_submit():
        # Buscamos al usuario en la base de datos por su cédula de identidad, tipo de documento y rol
        user = User.query.filter_by(id_card=form.id_card.data, id_card_type=form.id_card_type.data, role=form.role.data).first()
        # Si se encuentra al usuario y la contraseña es correcta
        if user and user.check_password(form.password.data):
            # Iniciamos la sesión del usuario
            session['user_id'] = user.id
            # Mostramos un mensaje de bienvenida
            flash(f'Bienvenido, {user.name}!', 'success')
            # Redirigimos al usuario al dashboard
            return redirect(url_for('dashboard'))
        # Si no se encuentra al usuario o la contraseña es incorrecta
        else:
            # Mostramos un mensaje de error
            flash('Inicio de sesión fallido, verifique sus credenciales', 'danger')
    # Si el formulario no se ha enviado o no es válido, renderizamos la plantilla de inicio de sesión con el formulario
    return render_template('login.html', form=form)

# Ruta para el dashboard, solo accesible si el usuario ha iniciado sesión
@app.route('/dashboard')
def dashboard():
    # Verificamos si el usuario ha iniciado sesión
    if 'user_id' in session:
        # Si el usuario ha iniciado sesión, obtenemos sus datos de la base de datos
        user = User.query.filter_by(id=session['user_id']).first()
        # Renderizamos la plantilla del dashboard con los datos del usuario
        return render_template('dashboard.html', user=user)
    # Si el usuario no ha iniciado sesión, lo redirigimos a la página de inicio de sesión
    else:
        return redirect(url_for('login'))

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    # Cerramos la sesión del usuario
    session.pop('user_id', None)
    # Redirigimos al usuario a la página de inicio de sesión
    return redirect(url_for('login'))

# Ruta para la página de inicio, redirige a la página de inicio de sesión
@app.route('/')
def index():
    # Redirigimos al usuario a la página de inicio de sesión
    return redirect(url_for('login'))

# Ejecutamos la aplicación si se ejecuta el archivo directamente
if __name__ == '__main__':
    # Ejecutamos la aplicación en modo debug
    app.run(debug=True)
