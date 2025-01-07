import sqlite3

# Conecta a la base de datos SQLite
connection = sqlite3.connect("LoginData.db")
cursor = connection.cursor()

# Comando SQL para crear la tabla USERS si no existe
cmd1 = """CREATE TABLE IF NOT EXISTS USERS (
            first_name varchar(50),
            last_name varchar(50),
            tipo_cedula varchar(1),
            cedula integer(15) primary key not null,
            email varchar(50),
            password varchar(50) not null)"""

# Ejecuta el comando SQL para crear la tabla
cursor.execute(cmd1)

# Comando SQL para insertar un usuario de prueba en la tabla USERS
cmd2 = """INSERT INTO USERS (first_name, last_name, cedula, tipo_cedula, email, password) 
          VALUES ('pepito', 'garcia', '1234567890', 'V', 'pepito@gmail.com', '12345')"""
# Ejecuta el comando SQL para insertar el usuario de prueba
cursor.execute(cmd2)
# Confirma los cambios en la base de datos
connection.commit()

# Ejecuta una consulta para seleccionar todos los usuarios de la tabla USERS
ans = cursor.execute("SELECT * FROM USERS").fetchall()

# Imprime cada usuario obtenido de la consulta
for i in ans:
    print(i)
