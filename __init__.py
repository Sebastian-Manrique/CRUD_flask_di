from routes import index
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def main():
    index()
    


if __name__ == '__main__':
    app.run(debug=True)
