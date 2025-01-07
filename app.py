from flask import Flask, render_template, request, redirect
import sqlite3
import os

# Crea una instancia de la aplicación Flask
app = Flask(__name__)
# Establece una clave secreta para la sesión
app.secret_key = os.urandom(24)

@app.route("/")
def login():
    # Renderiza la página de inicio de sesión
    return render_template("login.html")

@app.route("/login_validation", methods=["POST"])
def login_validation():
    # Obtiene el email y la contraseña del formulario de inicio de sesión
    cedula = request.form.get("cedula")
    password = request.form.get("password")

    # Conecta a la base de datos SQLite
    connection = sqlite3.connect("LoginData.db")
    cursor = connection.cursor()

    # Ejecuta una consulta para verificar si el usuario existe con el email y la contraseña proporcionados
    user = cursor.execute(
        "SELECT * FROM USERS WHERE cedula=? AND password=?", (cedula, password)
    ).fetchall()
    connection.close()
    
    # Cierra la conexión a la base de datos
    connection.close()
    
    # Si el usuario existe, redirige a la página de inicio con los datos del usuario
    if len(user) > 0:
        return redirect(
            f"/home?fname={user[0][0]}&lname={user[0][1]}&cedula={user[0][2]}&tipo_cedula={user[0][3]}&email={user[0][4]}"
        )
    else:
        # Si el usuario no existe, redirige de nuevo a la página de inicio de sesión
        return redirect("/")
    
@app.route('/signUp')
def signup():
    return render_template('signUp.html')

# -----------------------------------------------------------------------------------------------------------------------
@app.route("/home")
def home():
    # Obtiene el nombre del formulario de solicitud
    fname = request.args.get("fname")
    # Obtiene el apellido del formulario de solicitud
    lname = request.args.get("lname")
    # Obtiene la cedula del formulario
    cedula = request.args.get("cedula")
    # Obtiene el tipo de cedula del formulario
    tipo_cedula = request.args.get("tipo_cedula")
    # Obtiene el email del formulario de solicitud
    email = request.args.get("email")

    # Renderiza la plantilla 'home.html' pasando los valores obtenidos
    return render_template('home.html', fname=fname, lname=lname, cedula=cedula, tipo_cedula=tipo_cedula, email=email)

# -----------------------------------------------------------------------------------------------------------------------
@app.route('/add_user', methods=['POST'])
def add_user():
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    cedula = int(request.form.get("cedula"))
    tipo_cedula = request.form.get("tipo_cedula")
    email = request.form.get("email")
    password = request.form.get("password")

    connection = sqlite3.connect("LoginData.db")
    cursor = connection.cursor()

    ans = cursor.execute("select * from users where cedula=? AND password=?",(cedula, password )).fetchall()

    if len(ans) > 0:
        connection.close()
        return render_template('login.html')
    else:
        cursor.execute("INSERT INTO USERS (first_name, last_name, cedula, tipo_cedula, email, password ) values ( ?, ?, ?, ?, ?, ?)", (fname, lname, cedula, tipo_cedula, email,password))
        connection.commit()
        connection.close()
        return render_template('login.html')

if __name__ == "__main__":
    # Ejecuta la aplicación Flask en modo de depuración
    app.run(debug=True)
