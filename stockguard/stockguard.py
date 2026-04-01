"""StockGuard - Motor principal reexportado desde storage."""

from stockguard.storage import (
    add_item,
    get_total_value,
    load_inventory,
    save_inventory,
    update_price,
)

__all__ = [
    "add_item",
    "get_total_value",
    "load_inventory",
    "save_inventory",
    "update_price",
]
