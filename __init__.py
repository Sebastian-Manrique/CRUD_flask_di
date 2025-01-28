from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/juegos")
def juegos():
    return render_template('juegos.html')


@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/prueba")
def logiasdn():
    return render_template('prueba.html')

@app.route("/api/agarrarDatos")
def apiLlamada():
    contra = request.args.get("nombre", type=str)
    email = request.args.get("email", type=str)

    if contra == "any_":
        # Esto si es para todos los partidos, ya que tiene que hacer la peticion a otra API
        print(f"Estos son los datos, {contra} y {email}")


if __name__ == "__main__":
    app.run(debug=True)
