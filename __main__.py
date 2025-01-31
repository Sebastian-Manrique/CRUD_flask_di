from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3

app = Flask(__name__)
app.secret_key = '59e8a54219daca75ced6c672e77307e93efcdeae44cdc0279ab981d6086ded3a'

# Para encriptar y comprobar la contraseña from werkzeug. security import generate_password hash, check_password hash
# Añadir gif de carga a la hora de registrarse
# Comprobar que el correo no esta siendo ya usado
# Cambiar empleado por usuario
# Cuando cree un un usuario, que me rediriga a una pagina de "Todo ok"
# Añadir cosas de SQL Alchemy

# Inicializar el LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
# Redirige a la vista de login si no está autenticado
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/')
def main():
    return render_template('main.html')


@app.route("/inicio")
def juegos():
    return render_template('juegos.html')


@app.route("/registrate")
def registrarte():
    return render_template('registrate.html')


@app.route("/hecho")
def hecho():
    return render_template('hecho.html')


@app.route('/protected')
@login_required
def protected():
    return f'Hola, {current_user.id}! Esta es una página protegida.'


@app.route('/login', methods=['GET', 'POST'])
def login():
    leerUsuarios()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['CONTRASENA'] == password:
            user = User(email)
            login_user(user)
            return redirect(url_for('protected'))
        return 'Usuario o contraseña incorrectos'
    return render_template('login.html')


@app.route("/api/agarrarDatos")
def apiLlamada():
    contra = request.args.get("_contra", type=str)
    email = request.args.get("_email", type=str)
    print(f"Estos son los datos, contra: {contra} y email: {email}")
    return jsonify({"contra": contra, "email": email}), 200


@app.route("/api/crearCuenta")
def crearCuenta():
    usuario = request.args.get("_usuario", type=str)
    contra = request.args.get("_contra", type=str)
    email = request.args.get("_email", type=str)
    tipo = request.args.get("_tipo", type=str)

    crearUsuarioBD(usuario, contra, email, tipo)
    return jsonify({"usuario": usuario, "contra": contra, "email": email, "tipo": tipo}), 200


def crearUsuarioBD(usuario, contra, email, tipo):
    """SQLite y la tabla USUARIOS, parametros: ID, NOMBRE, CORREO,CONTRASENA, ADMIN"""
    if tipo == "Admin":
        admin = 1
    else:
        admin = 0
    try:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()

        # Insertar nuevo usuario
        cursor.execute("INSERT INTO USUARIOS (NOMBRE, CORREO, CONTRASENA, ADMIN) VALUES (?, ?, ?, ?)",
                       (usuario, email, contra, admin))

        conn.commit()
        print("Usuario insertado con éxito")

    except sqlite3.Error as error:
        print(f"Error al insertar usuario: {error}")

    finally:
        if conn:
            conn.close()


def leerUsuarios():
    global users
    users = {}
    try:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USUARIOS")
        rows = cursor.fetchall()
        for row in rows:
            users[row[2]] = {'name': row[1],
                             'password': row[3], 'admin': row[4]}
        print(users)
    except sqlite3.Error as error:
        print(f"Error al leer usuarios: {error}")

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    app.run(debug=True)
