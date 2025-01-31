# models.py
# Importamos la librería SQLAlchemy para trabajar con bases de datos
from flask_sqlalchemy import SQLAlchemy
# Importamos funciones para manejar contraseñas de forma segura
from werkzeug.security import generate_password_hash, check_password_hash

# Creamos una instancia de SQLAlchemy para nuestra aplicación
db = SQLAlchemy()

# Definimos una clase llamada 'User' que representa a un usuario en nuestra base de datos
class User(db.Model):
    # Cada atributo de la clase User se corresponde con una columna en la tabla 'user' de la base de datos
    
    # id: Columna para almacenar el ID único del usuario (autoincremental)
    id = db.Column(db.Integer, primary_key=True)
    # name: Columna para almacenar el nombre del usuario (no puede estar vacío)
    name = db.Column(db.String(80), nullable=False)
    # last_name: Columna para almacenar el apellido del usuario (no puede estar vacío)
    last_name = db.Column(db.String(80), nullable=False)
    # role: Columna para almacenar el rol del usuario (no puede estar vacío)
    role = db.Column(db.String(20), nullable=False)
    # id_card: Columna para almacenar el número de identificación del usuario (debe ser único y no puede estar vacío)
    id_card = db.Column(db.Integer, unique=True, nullable=False)
    # id_card_type: Columna para almacenar el tipo de identificación del usuario (no puede estar vacío)
    id_card_type = db.Column(db.String(1), nullable=False) 
    # email: Columna para almacenar el email del usuario (debe ser único y no puede estar vacío)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # password_hash: Columna para almacenar el hash de la contraseña del usuario (no puede estar vacío)
    password_hash = db.Column(db.String(128), nullable=False)

    # Método para establecer la contraseña del usuario de forma segura (hasheada)
    def set_password(self, password):
        # Se utiliza generate_password_hash para generar un hash de la contraseña 
        # y se guarda en el atributo password_hash
        self.password_hash = generate_password_hash(password)

    # Método para verificar si una contraseña ingresada coincide con la almacenada
    def check_password(self, password):
        # Se utiliza check_password_hash para comparar la contraseña ingresada con el hash almacenado
        # Devuelve True si coinciden, False en caso contrario
        return check_password_hash(self.password_hash, password)

