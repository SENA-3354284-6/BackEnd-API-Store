# src/config/mongo_config.py
"""Configuracion de conexion a MongoDB (equivalente a config/mongo.config.js)."""

import os

from dotenv import load_dotenv
from mongoengine import connect

from src.services.category_services import db_get_default_category

load_dotenv()


def db_connection():
    """Establece la conexion a MongoDB y crea la categoria por defecto."""
    from urllib.parse import urlparse

    db_uri = os.getenv("DB_URI") or "mongodb://localhost:27017/db-store"
    db_name = urlparse(db_uri).path.strip("/") or "db-store"
    try:
        connect(db=db_name, host=db_uri)
        print("Connected to MongoDB")
        # Inicializar la categoria por defecto si no existe en la base de datos
        db_get_default_category()
    except Exception as error:
        print(error)
        print("Connect Failed! :'(")
