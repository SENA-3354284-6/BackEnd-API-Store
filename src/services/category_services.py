# src/services/category_services.py
"""Servicio de Categoria (equivalente a services/category.services.js)."""

from src.models.category_model import Category


def insert_category(new_category):
    """Inserta una nueva categoria."""
    category = Category(**new_category)
    category.save()
    return category


def db_get_categories():
    """Obtiene todas las categorias."""
    return list(Category.objects())


def db_get_category_by_id(id):
    """Obtiene una categoria por su ID."""
    try:
        return Category.objects(id=id).first()
    except Exception:
        return None


def db_update_category(id, input_data):
    """Actualiza una categoria por su ID."""
    try:
        category = Category.objects(id=id).first()
    except Exception:
        return None
    if not category:
        return None

    for key, value in (input_data or {}).items():
        if hasattr(category, key):
            setattr(category, key, value)
    category.save()
    return category


def db_delete_category(id):
    """Elimina una categoria por su ID."""
    try:
        category = Category.objects(id=id).first()
    except Exception:
        return None
    if not category:
        return None
    category.delete()
    return category


def db_get_default_category():
    """Obtiene o crea la categoria por defecto 'Sin Categoría'."""
    try:
        category = Category.objects(
            slug="sin-categoria"
        ).first() or Category.objects(name="Sin Categoría").first()

        if not category:
            from datetime import datetime

            category = Category(
                name="Sin Categoría",
                slug="sin-categoria",
                description="Categoría asignada automáticamente a productos no categorizados",
                status=True,
                createdAt=datetime.utcnow(),
                updatedAt=datetime.utcnow(),
            )
            category.save()
            print('Categoría por defecto "Sin Categoría" (slug: sin-categoria) creada automáticamente')
        return category
    except Exception as error:
        print("Error al obtener/crear la categoría por defecto:", error)
        return None
