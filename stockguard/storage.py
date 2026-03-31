"""Módulo de persistencia del inventario para StockGuard.

Gestiona la lectura y escritura del inventario en disco,
con manejo robusto de errores de archivo y JSON corrupto.
"""

import json
import os
from typing import Any

from .validator import validate_qty, validate_price

INVENTORY_FILE = 'inventory.json'


def load_inventory(filepath: str = INVENTORY_FILE) -> list[dict[str, Any]]:
    """Carga el inventario desde un archivo JSON.

    Si el archivo no existe o está corrupto, devuelve una lista vacía
    en lugar de lanzar una excepción.

    Args:
        filepath (str): Ruta al archivo JSON del inventario.
            Por defecto usa INVENTORY_FILE.

    Returns:
        list[dict]: Lista de artículos del inventario.
            Devuelve [] si el archivo no existe o el JSON es inválido.

    Example:
        >>> items = load_inventory('inventory.json')
        >>> isinstance(items, list)
        True
    """
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_inventory(
    items: list[dict[str, Any]],
    filepath: str = INVENTORY_FILE
) -> None:
    """Guarda el inventario en un archivo JSON con formato legible.

    Args:
        items (list[dict]): Lista de artículos a persistir.
        filepath (str): Ruta al archivo JSON destino.
            Por defecto usa INVENTORY_FILE.

    Example:
        >>> save_inventory([{'name': 'Tornillo', 'qty': 10, 'price': 0.5}])
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


def add_item(
    name: str,
    qty: int,
    price: float,
    filepath: str = INVENTORY_FILE
) -> None:
    """Añade un nuevo artículo al inventario tras validar sus datos.

    Args:
        name (str): Nombre del artículo.
        qty (int): Cantidad en stock. Debe ser > 0.
        price (float): Precio unitario. Debe ser > 0.
        filepath (str): Ruta al archivo del inventario.

    Raises:
        ValueError: Si qty <= 0 o price <= 0.
        TypeError: Si qty no es int o price no es numérico.

    Example:
        >>> add_item('Tuerca', 50, 0.10)
    """
    if not validate_qty(qty):
        raise ValueError(f"qty debe ser mayor que 0, recibido: {qty}")
    if not validate_price(price):
        raise ValueError(f"price debe ser mayor que 0, recibido: {price}")
    items = load_inventory(filepath)
    items.append({'name': name, 'qty': qty, 'price': price})
    save_inventory(items, filepath)


def update_price(
    name: str,
    new_price: float,
    filepath: str = INVENTORY_FILE
) -> None:
    """Actualiza el precio de un artículo existente en el inventario.

    Args:
        name (str): Nombre del artículo a actualizar.
        new_price (float): Nuevo precio. Debe ser > 0.
        filepath (str): Ruta al archivo del inventario.

    Raises:
        ValueError: Si new_price <= 0.
        TypeError: Si new_price no es numérico.

    Example:
        >>> update_price('Tuerca', 0.15)
    """
    if not validate_price(new_price):
        raise ValueError(
            f"new_price debe ser mayor que 0, recibido: {new_price}"
        )
    items = load_inventory(filepath)
    for item in items:
        if item['name'] == name:
            item['price'] = new_price
    save_inventory(items, filepath)


def get_total_value(filepath: str = INVENTORY_FILE) -> float:
    """Calcula el valor total del inventario (suma de qty * price).

    Args:
        filepath (str): Ruta al archivo del inventario.

    Returns:
        float: Valor total del inventario. 0.0 si está vacío.

    Example:
        >>> get_total_value()
        0.0
    """
    return sum(
        i['qty'] * i['price'] for i in load_inventory(filepath)
    )