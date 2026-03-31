def validate_qty(qty: int) -> bool:
    """Valida que la cantidad de un ítem sea un entero positivo.

    Args:
        qty (int): Cantidad a validar.

    Returns:
        bool: True si qty > 0, False en caso contrario.

    Raises:
        TypeError: Si qty no es un entero.

    Example:
        >>> validate_qty(10)
        True
        >>> validate_qty(0)
        False
        >>> validate_qty(-5)
        False
    """
    if not isinstance(qty, int):
        raise TypeError(f"qty debe ser int, recibido {type(qty).__name__}")
    return qty > 0


def validate_price(price: float) -> bool:
    """Valida que el precio de un ítem sea un número positivo.

    Args:
        price (float): Precio a validar.

    Returns:
        bool: True si price > 0, False en caso contrario.

    Raises:
        TypeError: Si price no es int ni float.

    Example:
        >>> validate_price(9.99)
        True
        >>> validate_price(0)
        False
        >>> validate_price(-1.5)
        False
    """
    if not isinstance(price, (int, float)):
        raise TypeError(
            f"price debe ser int o float, recibido {type(price).__name__}"
        )
    return price > 0