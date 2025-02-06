from werkzeug.security import generate_password_hash, check_password_hash
from models import Juego
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

# 2. Para encriptar y comprobar la contraseña from werkzeug. security import generate_password hash, check_password hash
# Añadir una pagina para "usurio o contraseña incorrecta"
# Añadir si pasa el raton cerca de las burbujas estan se muevan.

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
    juegos = 0

    esAdmin = usuario.admin
    if esAdmin == 1:
        juegos = Juego.query.all()
    else:
        juegos = Juego.query.filter_by(usuario_id=current_user.id).all()

    return render_template('juegos.html', usuario=usuario, juegos=juegos)


@app.route('/api/juegos', methods=['GET'])
@login_required
def obtener_juegos():
    usuario = Usuario.query.filter_by(id=current_user.id).first()

    if usuario.admin:
        juegos = Juego.query.all()
    else:
        juegos = Juego.query.filter_by(usuario_id=current_user.id).all()

    juegos_json = [{
        'id': juego.id,
        'nombre': juego.nombre,
        'precio': juego.precio,
        'descripcion': juego.descripcion,
        'usuario_id': juego.usuario_id
    } for juego in juegos]

    return jsonify(juegos_json)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        admin = 1 if role == "admin" else 0

        usuario = Usuario.query.filter_by(correo=email).first()

        # Verifica la contraseña encriptada
        if usuario and check_password_hash(usuario.contrasena, password):
            login_user(usuario)
            return redirect(url_for('protected'))

        # Retorna un error 401 si falla el login
        return 'Usuario o contraseña incorrectos', 401

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

    # Encriptar la contraseña antes de guardarla
    hashed_password = generate_password_hash(contra)

    # Guardamos la contraseña encriptada
    if crearUsuarioBD(usuario, hashed_password, email, tipo):
        return jsonify({"usuario": usuario, "email": email, "tipo": tipo}), 200
    else:
        return jsonify({"message": "Error, correo ya en uso"}), 409


def crearUsuarioBD(usuario, contra, email, tipo):
    """SQLite y la tabla USUARIOS, parametros: ID, NOMBRE, CORREO,CONTRASENA, ADMIN"""

    correo = Usuario.query.filter_by(correo=email).first()

    if correo:
        return False
    else:

        admin = True if tipo == "Admin" else False
        try:
            # Crear una instancia del nuevo usuario
            nuevo_usuario = Usuario(
                nombre=usuario, correo=email, contrasena=contra, admin=admin)

            # Agregar el nuevo usuario a la sesión
            db.session.add(nuevo_usuario)

            # Confirmar la transacción
            db.session.commit()

            return True
            # DEBUG, Verificar que el usuario se haya insertado
            # usuario_insertado = Usuario.query.filter_by(correo=email).first()
            # if usuario_insertado:
            #     print(
            #         f"Usuario {usuario_insertado.nombre} insertado correctamente en la base de datos.")
            # else:
            #     print("Error: El usuario no se insertó en la base de datos.")

        except Exception as error:
            print(f"Error al insertar usuario: {error}")
            db.session.rollback()  # Revertir en caso de error

        finally:
            db.session.close()


@app.route("/api/crearJuego")
def crearJuego():
    # Llamada de API para crear un juego
    nombre = request.args.get("_nombre", type=str)
    precio = request.args.get("_precio", type=float)
    descripcion = request.args.get("_dscrp", type=str)
    usuario_id = request.args.get("_userId", type=int)

    respuesta = crear_juego(nombre, precio, descripcion, usuario_id)

    print(respuesta)
    return respuesta


def crear_juego(nombre, precio, descripcion, usuario_id):
    # La funcion para añadirlo a la BDD
    if not all([nombre, descripcion]) or precio is None:
        return jsonify({"error": "Faltan datos"}), 400

    nuevo_juego = Juego(
        nombre=nombre,
        precio=precio,
        descripcion=descripcion,
        usuario_id=usuario_id
    )

    try:
        db.session.add(nuevo_juego)
        db.session.commit()
        return jsonify({"success": True, "message": "Juego creado exitosamente"}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 500


@app.route("/api/modificarJuego")
def modificarJuego():
    # Llamada de API para modificar un juego
    juego_id = request.args.get("_id", type=int)
    nombre = request.args.get("_nombre", type=str)
    precio = request.args.get("_precio", type=float)
    descripcion = request.args.get("_dscrp", type=str)

    respuesta = modificar_juego(juego_id, nombre, precio, descripcion)

    print(respuesta)
    return respuesta


def modificar_juego(juego_id, nombre, precio, descripcion):
    # La funcion para modificar un juego de la BDD
    if not all([juego_id, nombre, descripcion]) or precio is None:
        print(juego_id, nombre, precio, descripcion)
        return jsonify({"error": "Faltan datos"}), 400

    # Buscar el juego en la base de datos
    juego_a_modificar = Juego.query.filter_by(id=juego_id).first()

    if not juego_a_modificar:
        return jsonify({"error": "Juego no encontrado"}), 404

    try:
        # Modificar los valores del juego
        juego_a_modificar.nombre = nombre
        juego_a_modificar.precio = precio
        juego_a_modificar.descripcion = descripcion

        # Guardar los cambios en la base de datos
        db.session.commit()

        return jsonify({"success": True, "message": "Juego modificado exitosamente"}), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 500


@app.route("/api/eliminarJuego")
def eliminarJuego():
    # Llamada de API para modificar un juego
    juego_id = request.args.get("_id", type=int)

    respuesta = eliminar_juego(juego_id)

    print(respuesta)
    return respuesta


def eliminar_juego(juego_id):
    # La funcion para modificar un juego de la BDD
    if not all([juego_id]):
        print(juego_id)
        return jsonify({"error": "Faltan datos"}), 400

    # Buscar el juego en la base de datos
    juego_a_modificar = Juego.query.filter_by(id=juego_id).first()

    if not juego_a_modificar:
        return jsonify({"error": "Juego no encontrado"}), 404

    try:
        # Elimina el juego de la BDD
        db.session.delete(juego_a_modificar)
        db.session.commit()

        return jsonify({"success": True, "message": "Juego eliminado exitosamente"}), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 500


@app.route("/get_juegos", methods=['GET'])
# Recargar la tabla de juegos
def get_juegos():
    # Consulta todos los juegos de la base de datos
    juegos = Juego.query.all()

    # Crear una lista de diccionarios con los datos de cada juego
    juegos_list = [{
        'id': juego.id,
        'nombre': juego.nombre,
        'precio': juego.precio,
        'descripcion': juego.descripcion,
        'usuario_id': juego.usuario_id
    } for juego in juegos]

    # Retornar los datos en formato JSON
    # print(juegos_list)
    return jsonify(juegos_list)


if __name__ == "__main__":
    app.run(debug=True)
