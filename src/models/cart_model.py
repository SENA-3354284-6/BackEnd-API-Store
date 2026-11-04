# src/models/cart_model.py
"""Modelos de Carrito de Compras (equivalente a models/cart/*.js)."""

from datetime import datetime

from mongoengine import (
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    IntField,
    ListField,
    ReferenceField,
)

from src.models.product_model import Product
from src.models.user_model import User


class CartItem(EmbeddedDocument):
    product = ReferenceField(Product, required=True)
    quantity = IntField(required=True, min_value=1, default=1)


class Cart(Document):
    user = ReferenceField(User, required=True, unique=True)
    items = ListField(EmbeddedDocumentField(CartItem), default=list)

    createdAt = DateTimeField(default=datetime.utcnow)
    updatedAt = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "cart"}

    def save(self, *args, **kwargs):
        self.updatedAt = datetime.utcnow()
        if not self.createdAt:
            self.createdAt = datetime.utcnow()
        return super().save(*args, **kwargs)
