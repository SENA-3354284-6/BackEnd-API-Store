import mongomock
import pytest
from flask import Flask
from mongoengine import connect

from src.helpers.jwt_helper import generate_token
from src.models.category_model import Category
from src.models.user_model import User
from src.routes.category_routes import category_bp

API_CATEGORIES_URL = "/api/categories"


@pytest.fixture
def app():
    """App Flask con el blueprint de categorias para pruebas de integracion."""
    application = Flask(__name__)
    application.config["TESTING"] = True
    application.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024
    application.register_blueprint(category_bp, url_prefix=API_CATEGORIES_URL)
    connect(db="db_store_integration_tests", alias="default", mongo_client_class=mongomock.MongoClient)
    return application


@pytest.fixture
def clean_database():
    """Limpia las colecciones de categorias y usuarios entre pruebas."""
    yield
    Category.objects.delete()
    User.objects.delete()


@pytest.fixture
def client(app, clean_database):
    """Cliente de pruebas de Flask (test client) para simular peticiones HTTP."""
    return app.test_client()


@pytest.fixture
def admin_token(clean_database):
    """Token JWT valido para un usuario con rol de administrador."""
    user = User(
        name="Admin Integration",
        nickname="adminint",
        email="admin.integration@store.com",
        password="Secret123",
        role="administrator",
        status=True,
    ).save()

    token = generate_token({
        "_id": str(user.id),
        "name": user.name,
        "nickname": user.nickname,
        "email": user.email,
        "role": user.role,
        "avatar": user.avatarUrl,
        "status": user.status,
    })

    return token


@pytest.fixture
def subscriber_token(clean_database):
    """Token JWT valido para un usuario con rol de subscriptor."""
    user = User(
        name="Subscriber Integration",
        nickname="subint",
        email="subscriber.integration@store.com",
        password="Secret123",
        role="subscriber",
        status=True,
    ).save()

    token = generate_token({
        "_id": str(user.id),
        "name": user.name,
        "nickname": user.nickname,
        "email": user.email,
        "role": user.role,
        "avatar": user.avatarUrl,
        "status": user.status,
    })

    return token
