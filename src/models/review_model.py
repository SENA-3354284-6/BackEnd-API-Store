# src/models/review_model.py
"""Modelo de Resena (equivalente a models/review.model.js)."""

from datetime import datetime

from mongoengine import (
    DateTimeField,
    Document,
    IntField,
    ReferenceField,
    StringField,
)

from src.models.product_model import Product
from src.models.user_model import User


class Review(Document):
    ownerUserId = ReferenceField(User, required=True)
    productId = ReferenceField(Product, required=True)
    rating = IntField(required=True, min_value=1, max_value=5)
    comment = StringField(required=True)

    createdAt = DateTimeField(default=datetime.utcnow)
    updatedAt = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "reviews"}

    def save(self, *args, **kwargs):
        self.updatedAt = datetime.utcnow()
        if not self.createdAt:
            self.createdAt = datetime.utcnow()
        return super().save(*args, **kwargs)
