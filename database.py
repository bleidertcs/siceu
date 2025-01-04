import sqlite3

# Conecta a la base de datos SQLite
connection = sqlite3.connect("LoginData.db")
cursor = connection.cursor()

# Comando SQL para crear la tabla USERS si no existe
cmd1 = """CREATE TABLE IF NOT EXISTS USERS (
            first_name varchar(50),
            last_name varchar(50),
            email varchar(50) primary key,
            password varchar(50) not null)"""

# Ejecuta el comando SQL para crear la tabla
cursor.execute(cmd1)

# Comando SQL para insertar un usuario de prueba en la tabla USERS
cmd2 = """INSERT INTO USERS (first_name, last_name, email, password) 
          VALUES ('tester', 'test', 'tester@gmail.com', 'tester')"""
# Ejecuta el comando SQL para insertar el usuario de prueba
cursor.execute(cmd2)
# Confirma los cambios en la base de datos
connection.commit()

# Ejecuta una consulta para seleccionar todos los usuarios de la tabla USERS
ans = cursor.execute("SELECT * FROM USERS").fetchall()

# Imprime cada usuario obtenido de la consulta
for i in ans:
    print(i)
