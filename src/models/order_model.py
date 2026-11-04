# src/models/order_model.py
"""Modelos de Orden de Compra (equivalente a models/order/*.js)."""

import random
import time
from datetime import datetime

from mongoengine import (
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

from src.models.product_model import Product
from src.models.user_model import User


class OrderItem(EmbeddedDocument):
    product = ReferenceField(Product, required=True)
    name = StringField(required=True)
    price = FloatField(required=True, min_value=0)
    quantity = IntField(required=True, min_value=1)


class ShippingAddress(EmbeddedDocument):
    address = StringField(required=True)
    city = StringField(required=True)
    phone = StringField(required=True)
    notes = StringField(default="")


class Order(Document):
    user = ReferenceField(User, required=True)
    items = ListField(EmbeddedDocumentField(OrderItem), required=True)
    shippingAddress = EmbeddedDocumentField(ShippingAddress, required=True)
    totalAmount = FloatField(required=True, min_value=0)
    status = StringField(
        choices=["PENDING", "PAID", "SHIPPED", "DELIVERED", "CANCELLED"],
        default="PAID",
    )
    paymentMethod = StringField(
        choices=["MOCK_CARD", "CASH_ON_DELIVERY", "WOMPI", "PAYPAL"],
        default="MOCK_CARD",
    )
    transactionId = StringField(
        default=lambda: f"TX-{int(time.time() * 1000)}-{random.randint(1000, 9999)}"
    )

    createdAt = DateTimeField(default=datetime.utcnow)
    updatedAt = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "order"}

    def clean(self):
        if not self.items or len(self.items) == 0:
            raise ValidationError("Una orden debe contener al menos un producto")

    def save(self, *args, **kwargs):
        self.updatedAt = datetime.utcnow()
        if not self.createdAt:
            self.createdAt = datetime.utcnow()
        self.validate(clean=True)
        return super().save(*args, **kwargs)
