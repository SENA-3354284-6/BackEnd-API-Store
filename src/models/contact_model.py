# src/models/contact_model.py
"""Modelo de Contacto (equivalente a models/contact.model.js)."""

from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    ReferenceField,
    StringField,
)

from src.models.user_model import User


class Contact(Document):
    userId = ReferenceField(User, required=True)
    label = StringField(required=True, max_length=30)
    receiverName = StringField(required=True, min_length=2, max_length=50)
    address = StringField(required=True, min_length=5)
    phone = StringField(required=True, regex=r"^[+0-9\s-]+$")
    isDefault = BooleanField(default=False)

    createdAt = DateTimeField(default=datetime.utcnow)
    updatedAt = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "contact"}

    def save(self, *args, **kwargs):
        self.updatedAt = datetime.utcnow()
        if not self.createdAt:
            self.createdAt = datetime.utcnow()
        return super().save(*args, **kwargs)
