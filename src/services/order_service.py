# src/services/order_service.py
"""Servicio de Ordenes (equivalente a services/order.service.js)."""

from src.models.cart_model import Cart
from src.models.order_model import Order, OrderItem, ShippingAddress
from src.models.product_model import Product


def _extract_product_id(value):
    if isinstance(value, dict):
        return value.get("_id") or value.get("id") or value.get("product")
    if hasattr(value, "id"):
        return value.id
    return value


def _to_number(value):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return 0


def db_create_order(user_id, order_payload):
    """Crea una nueva orden de compra."""
    shipping_address = order_payload.get("shippingAddress")
    payment_method = order_payload.get("paymentMethod")
    direct_items = order_payload.get("items")

    items_to_process = []

    if isinstance(direct_items, list) and len(direct_items) > 0:
        items_to_process = direct_items
    else:
        user_cart = Cart.objects(user=user_id).first()
        if not user_cart or not user_cart.items or len(user_cart.items) == 0:
            raise Exception("El carrito de compras está vacío")

        items_to_process = [
            {
                "product": (
                    str(item.product.id)
                    if hasattr(item.product, "id")
                    else str(item.product)
                ),
                "quantity": item.quantity,
            }
            for item in user_cart.items
        ]

    order_items = []
    calculated_total = 0.0
    products_to_update = []

    for item in items_to_process:
        product_id = _extract_product_id(item.get("product"))
        requested_qty = _to_number(item.get("quantity"))

        if not product_id or requested_qty <= 0:
            continue

        try:
            product = Product.objects(id=product_id).first()
        except Exception:
            product = None

        if not product or not product.status:
            raise Exception("El producto no está disponible en la tienda")

        if product.stock < requested_qty:
            raise Exception(
                f'Stock insuficiente para "{product.name}". Disponible: {product.stock}, Solicitado: {requested_qty}'
            )

        item_subtotal = product.price * requested_qty
        calculated_total += item_subtotal

        order_items.append(OrderItem(
            product=product,
            name=product.name,
            price=product.price,
            quantity=requested_qty,
        ))

        products_to_update.append({
            "productId": product.id,
            "quantityToDeduct": requested_qty,
        })

    if len(order_items) == 0:
        raise Exception("No se encontraron productos válidos para procesar la orden")

    # Descontar stock
    for prod in products_to_update:
        try:
            product = Product.objects(id=prod["productId"]).first()
            if product:
                product.stock = max(0, product.stock - prod["quantityToDeduct"])
                product.save()
        except Exception:
            pass

    # Crear direccion de envio
    shipping = ShippingAddress(
        address=shipping_address.get("address", "").strip(),
        city=shipping_address.get("city", "").strip(),
        phone=shipping_address.get("phone", "").strip(),
        notes=shipping_address.get("notes", "") if shipping_address else "",
    )

    new_order = Order(
        user=user_id,
        items=order_items,
        shippingAddress=shipping,
        totalAmount=calculated_total,
        paymentMethod=payment_method or "MOCK_CARD",
        status="PAID",
    )
    new_order.save()

    # Vaciar carrito
    Cart.objects(user=user_id).update_one(set__items=[])

    return Order.objects(id=new_order.id).first()


def db_get_orders_by_user_id(user_id):
    """Obtiene el historial de ordenes de un usuario."""
    try:
        return list(Order.objects(user=user_id).order_by("-createdAt"))
    except Exception:
        return list(Order.objects(user=user_id).order_by("-createdAt"))


def db_get_order_by_id(order_id, user_id):
    """Obtiene el detalle de una orden por su ID."""
    try:
        return Order.objects(id=order_id, user=user_id).first()
    except Exception:
        return None
