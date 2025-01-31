from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, orm
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from models import Usuario, db

Base = orm.declarative_base()


# Configura tu motor y sesión de SQLAlchemy
DATABASE_URL = "sqlite:///usuarios.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def leerUsuarios():
    global users
    users = {}
    try:
        # Query para obtener todos los usuarios
        usuarios = session.query(Usuario).all()
        for usuario in usuarios:
            users[usuario.correo] = {
                'NOMBRE': usuario.nombre,
                'CONTRASENA': usuario.contrasena,
                'ADMIN': usuario.admin
            }
        # print(users)
    except Exception as error:
        print(f"Error al leer usuarios: {error}")
    finally:
        session.close()

    return users