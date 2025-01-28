from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from decrypt import decrypt_data

app = Flask(__name__)
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


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/juegos")
def juegos():
    return render_template('juegos.html')


@app.route("/registrarte")
def registrarte():
    return render_template('registrarte.html')


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


@app.route("/prueba")
def logiasdn():
    return render_template('prueba.html')


@app.route("/api/agarrarDatos")
def apiLlamada():
    contra = request.args.get("_contra", type=str)
    email = request.args.get("_email", type=str)

    if contra == "any_":
        # Esto si es para todos los partidos, ya que tiene que hacer la peticion a otra API
        print(f"Estos son los datos, {contra} y {email}")
        return jsonify({"message": "Datos mal recibidos"}), 200
    else:
        print(
            f"Estos son los datos, contra: {contra} y email: {email}")
        print(
            f"Estos son los datos, {contra} y {email}")
        return jsonify({"message": "Datos recibidos correctamente", "contra": contra, "email": email}), 200


if __name__ == "__main__":
    app.run(debug=True)
