# src/services/product_service.py
"""Servicio de Producto (equivalente a services/product.service.js)."""

from src.models.product_model import Product


def db_create_product(new_product):
    """Crea un producto y puebla la categoria."""
    product = Product(**new_product)
    product.save()
    return product


def db_get_products():
    """Obtiene todos los productos con su categoria."""
    return list(Product.objects())


def db_get_product_by_id(id):
    """Obtiene un producto por su ID con su categoria."""
    try:
        return Product.objects(id=id).first()
    except Exception:
        return None


def db_delete_product(id):
    """Elimina un producto por su ID y retorna el documento eliminado."""
    try:
        product = Product.objects(id=id).first()
    except Exception:
        return None
    if not product:
        return None
    product.delete()
    return product


def db_update_product(id, input_data):
    """Actualiza un producto por su ID."""
    try:
        product = Product.objects(id=id).first()
    except Exception:
        return None
    if not product:
        return None

    for key, value in (input_data or {}).items():
        if hasattr(product, key):
            setattr(product, key, value)
    product.save()
    return product
