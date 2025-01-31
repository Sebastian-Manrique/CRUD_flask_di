from dbManager import DATABASE_URL, engine, Session
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from routes import simple_page
from flask_sqlalchemy import SQLAlchemy
from models import Usuario, db

app = Flask(__name__)
app.secret_key = '59e8a54219daca75ced6c672e77307e93efcdeae44cdc0279ab981d6086ded3a'
app.register_blueprint(simple_page)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Añadir si pasa el raton cerca de las burbujas estan se muevan
# Añadir funcionalidad de juegos para que se muestren y se añadan a la base de datos
# Para encriptar y comprobar la contraseña from werkzeug. security import generate_password hash, check_password hash
# Comprobar que el correo no esta siendo ya usado
# Cambiar empleado por usuario
# Cuando cree un un usuario, que me rediriga a una pagina de "Todo ok"

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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('main.html')


@app.route('/protected')
@login_required
def protected():
    usuario = Usuario.query.filter_by(id=current_user.id).first()
    return render_template('juegos.html', usuario=usuario)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        usuario = Usuario.query.filter_by(correo=email).first()
        if usuario and usuario.contrasena == password:
            login_user(usuario)
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
    admin = True if tipo == "Admin" else False
    try:
        # Crear una instancia del nuevo usuario
        nuevo_usuario = Usuario(
            nombre=usuario, correo=email, contrasena=contra, admin=admin)

        # Agregar el nuevo usuario a la sesión
        db.session.add(nuevo_usuario)

        # Confirmar la transacción
        db.session.commit()
        print("Usuario insertado con éxito")

        # Verificar que el usuario se haya insertado
        usuario_insertado = Usuario.query.filter_by(correo=email).first()
        if usuario_insertado:
            print(
                f"Usuario {usuario_insertado.nombre} insertado correctamente en la base de datos.")
        else:
            print("Error: El usuario no se insertó en la base de datos.")

    except Exception as error:
        print(f"Error al insertar usuario: {error}")
        db.session.rollback()  # Revertir en caso de error

    finally:
        db.session.close()


if __name__ == "__main__":
    app.run(debug=True)
