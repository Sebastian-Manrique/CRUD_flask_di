from flask import render_template, request, redirect, url_for, Blueprint, abort
from jinja2 import TemplateNotFound
from flask_login import login_user, logout_user, login_required, current_user

simple_page = Blueprint('simple_page', __name__, template_folder='templates')


@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        return render_template(f'main.html')
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
