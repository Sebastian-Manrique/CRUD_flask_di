from flask import render_template, request, redirect, url_for, Blueprint, abort
from jinja2 import TemplateNotFound
from flask_login import login_user, logout_user, login_required, current_user
from models import Usuario
simple_page = Blueprint('simple_page', __name__, template_folder='templates')


@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        usuario = None
        if current_user.is_authenticated:  # Verifica si el usuario está logueado
            usuario = Usuario.query.get(current_user.id)

        return render_template('main.html', usuario=usuario)
    except TemplateNotFound:
        abort(404)


@simple_page.route('/registrate', defaults={'page': 'index'})
@simple_page.route('/<page>')
def registrarte(page):
    try:
        return render_template('registrate.html')

    except TemplateNotFound:
        abort(404)


@simple_page.route('/hecho', defaults={'page': 'index'})
@simple_page.route('/<page>')
def hecho(page):
    try:
        return render_template('hecho.html')

    except TemplateNotFound:
        abort(404)
