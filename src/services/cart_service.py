# src/services/cart_service.py
"""Servicio de Carrito de Compras (equivalente a services/cart.service.js)."""

from src.models.cart_model import Cart, CartItem
from src.models.product_model import Product


def db_get_cart_by_user_id(user_id):
    """Obtiene el carrito de un usuario; si no existe, crea uno vacio."""
    try:
        cart = Cart.objects(user=user_id).first()
    except Exception:
        cart = None
    if not cart:
        cart = Cart(user=user_id, items=[])
        cart.save()
        cart = Cart.objects(id=cart.id).first()
    return cart


def db_update_cart(user_id, items=None):
    """Actualiza los elementos del carrito validando stock y estado."""
    if items is None:
        items = []
    raw_items = [item for item in items if _to_number(item.get("quantity")) > 0]
    valid_items = []

    for item in raw_items:
        product_id = item.get("product")
        try:
            product = Product.objects(id=product_id).first()
        except Exception:
            product = None

        if not product or not product.status or (product.stock or 0) <= 0:
            continue

        allowed_quantity = min(_to_number(item.get("quantity")), product.stock)
        if allowed_quantity > 0:
            valid_items.append(CartItem(product=product, quantity=allowed_quantity))

    cart = Cart.objects(user=user_id).first()
    if not cart:
        cart = Cart(user=user_id, items=[])
    cart.items = valid_items
    cart.save()

    return Cart.objects(id=cart.id).first()


def db_sync_cart(user_id, guest_items=None):
    """Fusiona el carrito anonimo con el del usuario autenticado."""
    if guest_items is None:
        guest_items = []
    cart = Cart.objects(user=user_id).first()
    if not cart:
        cart = Cart(user=user_id, items=[])

    for guest_item in guest_items:
        if not guest_item.get("product") or not guest_item.get("quantity"):
            continue
        try:
            product = Product.objects(id=guest_item.get("product")).first()
        except Exception:
            product = None
        if not product or not product.status or (product.stock or 0) <= 0:
            continue

        product_id_str = str(guest_item.get("product"))
        existing_index = None
        for idx, item in enumerate(cart.items):
            if str(item.product.id if hasattr(item.product, "id") else item.product) == product_id_str:
                existing_index = idx
                break

        if existing_index is not None:
            new_quantity = cart.items[existing_index].quantity + _to_number(guest_item.get("quantity"))
            cart.items[existing_index].quantity = min(new_quantity, product.stock)
        else:
            initial_quantity = min(_to_number(guest_item.get("quantity")), product.stock)
            if initial_quantity > 0:
                cart.items.append(CartItem(product=product, quantity=initial_quantity))

    cart.save()
    return Cart.objects(id=cart.id).first()


def db_remove_item_from_cart(user_id, product_id):
    """Elimina un producto del carrito del usuario."""
    cart = Cart.objects(user=user_id).first()
    if not cart:
        return None
    cart.items = [item for item in cart.items
                  if str(item.product.id if hasattr(item.product, "id") else item.product) != str(product_id)]
    cart.save()
    return Cart.objects(id=cart.id).first()


def db_clear_cart(user_id):
    """Vacia el carrito del usuario."""
    cart = Cart.objects(user=user_id).first()
    if not cart:
        cart = Cart(user=user_id, items=[])
        cart.save()
    else:
        cart.items = []
        cart.save()
    return Cart.objects(id=cart.id).first()


def _to_number(value):
    try:
        return int(value) if isinstance(value, (int, float, str)) and str(value).replace(".", "", 1).isdigit() else 0
    except (ValueError, TypeError):
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return 0
