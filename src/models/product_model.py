# src/models/product_model.py
"""Modelo de Producto (equivalente a models/product.model.js)."""

from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    FloatField,
    IntField,
    ListField,
    ReferenceField,
    StringField,
    ValidationError,
)

from src.models.category_model import Category


class ProductImage(EmbeddedDocument):
    """Imagen asociada a un producto (url + isMain)."""

    url = StringField(required=True)
    isMain = BooleanField(default=False)


class Product(Document):
    referenceCode = StringField(required=True, unique=True)
    name = StringField(
        required=True,
        min_length=3,
        unique=True,
    )
    description = StringField(max_length=500)
    price = FloatField(min_value=0, default=0)
    stock = IntField(min_value=0, default=1)
    status = BooleanField(default=True)
    category = ReferenceField(Category, required=True)
    images = ListField(EmbeddedDocumentField(ProductImage))

    createdAt = DateTimeField(default=datetime.utcnow)
    updatedAt = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "product"}

    def clean(self):
        # Validacion equivalente a Mongoose: maximo 9 imagenes
        if self.images is not None and len(self.images) > 9:
            raise ValidationError("No se pueden asociar mas de nueve (9) imagenes a un producto")

    def save(self, *args, **kwargs):
        self.updatedAt = datetime.utcnow()
        if not self.createdAt:
            self.createdAt = datetime.utcnow()
        self.validate(clean=True)
        return super().save(*args, **kwargs)
