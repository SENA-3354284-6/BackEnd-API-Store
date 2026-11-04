# src/models/user_model.py
"""Modelo de Usuario (equivalente a models/user.model.js)."""

from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    EmailField,
    StringField,
)

from src.config.global_config import ALLOWED_ROLES, ROLES

# Expresiones regulares equivalentes a las del Schema de Mongoose
NAME_REGEX = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"
NICKNAME_REGEX = r"^[a-zA-Z0-9]+$"
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


class User(Document):
    # Estructura de datos del usuario
    name = StringField(
        required=True,
        regex=NAME_REGEX,
        min_length=2,
        max_length=50,
    )
    nickname = StringField(
        required=True,
        unique=True,
        min_length=3,
        max_length=20,
        regex=NICKNAME_REGEX,
    )
    email = EmailField(required=True, unique=True, regex=EMAIL_REGEX)
    password = StringField(required=True)
    role = StringField(
        required=True,
        choices=ALLOWED_ROLES,
        default=ROLES["SUBSCRIBER"],
    )
    status = BooleanField(default=True)
    avatarUrl = StringField(default="uploads/avatars/default-avatar.png")

    # Timestamps (Mongoose timestamps: true)
    createdAt = DateTimeField(default=datetime.utcnow)
    updatedAt = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "user", "timestamps": False}

    def save(self, *args, **kwargs):
        # Actualizar manualmente la fecha de modificacion
        self.updatedAt = datetime.utcnow()
        if not self.createdAt:
            self.createdAt = datetime.utcnow()
        return super().save(*args, **kwargs)
