# src/models/category_model.py
"""Modelo de Categoria (equivalente a models/category.model.js)."""

from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    ReferenceField,
    StringField,
)

from src.models.user_model import User


class Category(Document):
    name = StringField(
        required=True,
        unique=True,
        min_length=5,
        max_length=100,
    )
    slug = StringField(required=True, unique=True)
    description = StringField(default="")
    urlImage = StringField(default="/uploads/categories/default-category.png")
    status = BooleanField(default=True)
    createdBy = ReferenceField(User, null=True)

    createdAt = DateTimeField(default=datetime.utcnow)
    updatedAt = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "category"}

    def save(self, *args, **kwargs):
        self.updatedAt = datetime.utcnow()
        if not self.createdAt:
            self.createdAt = datetime.utcnow()
        # Auto-generar slug si no viene definido (compatibilidad basica)
        if not self.slug and self.name:
            self.slug = self.name
        return super().save(*args, **kwargs)
