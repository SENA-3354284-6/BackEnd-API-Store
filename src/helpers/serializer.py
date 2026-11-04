# src/helpers/serializer.py
"""Utilidad para convertir documentos MongoEngine a diccionarios JSON serializables
(equivalente a toObject()/toJSON() de Mongoose)."""


from datetime import datetime

from bson import ObjectId
from mongoengine import Document, EmbeddedDocument, ReferenceField


def to_serializable(value):
    """Convierte de forma recursiva un valor MongoEngine/BSON a tipos JSON."""
    if value is None:
        return None

    if isinstance(value, Document):
        data = {}
        for field_name in value._fields.keys():
            field_value = getattr(value, field_name, None)
            key = "_id" if field_name == "id" else field_name
            data[key] = to_serializable(field_value)
        return data

    if isinstance(value, EmbeddedDocument):
        data = {}
        for field_name in value._fields.keys():
            field_value = getattr(value, field_name, None)
            key = "_id" if field_name == "id" else field_name
            data[key] = to_serializable(field_value)
        return data

    if isinstance(value, ObjectId):
        return str(value)

    if isinstance(value, datetime):
        return value.isoformat()

    if isinstance(value, list):
        return [to_serializable(item) for item in value]

    if isinstance(value, tuple):
        return [to_serializable(item) for item in value]

    if isinstance(value, dict):
        return {key: to_serializable(val) for key, val in value.items()}

    # mongoengine ReferenceField puede devolver el documento directamente;
    # si es aun un DBRef/ObjectId, ya fue cubierto arriba.
    return value
