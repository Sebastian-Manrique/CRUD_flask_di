from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3

app = Flask(__name__,  template_folder='templates')
app.config['SECRET_KEY'] = '59e8a54219daca75ced6c672e77307e93efcdeae44cdc0279ab981d6086ded3a'

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


@app.route("/juegos")
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
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            user = User(email)
            login_user(user)
            return redirect(url_for('protected'))
        return 'Usuario o contraseña incorrectos'
    return render_template('login.html')


@app.route("/api/agarrarDatos")
def apiLlamada():
    contra = request.args.get("_contra", type=str)
    email = request.args.get("_email", type=str)

    if contra == "any_":
        # Esto si es para todos los partidos, ya que tiene que hacer la peticion a otra API
        print(f"Estos son los datos, {contra} y {email}")
        return jsonify({"message": "Datos mal recibidos"}), 200
    else:
        print(f"Estos son los datos, contra: {contra} y email: {email}")
        return jsonify({"contra": contra, "email": email}), 200


@app.route("/api/crearCuenta")
def crearCuenta():
    usuario = request.args.get("_usuario", type=str)
    contra = request.args.get("_contra", type=str)
    email = request.args.get("_email", type=str)

    crearBD(usuario, contra, email)
    return jsonify({"usuario": usuario, "contra": contra, "email": email}), 200


def crearBD(usuario, contra, email):
    """SQLite y la tabla USUARIOS, parametros: ID, NOMBRE, CORREO,CONTRASENA, PUNTUACION"""
    try:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()

        # Insertar nuevo usuario
        cursor.execute("INSERT INTO USUARIOS (NOMBRE, CORREO, CONTRASENA) VALUES (?, ?, ?)",
                       (usuario, email, contra))

        conn.commit()
        print("Usuario insertado con éxito")

    except sqlite3.Error as error:
        print(f"Error al insertar usuario: {error}")

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    app.run(debug=True)
