import json
import os
 
INVENTORY_FILE = 'inventory.json'
 
def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return []
    with open(INVENTORY_FILE) as f:
        return json.load(f)   # ⚠ sin manejo de JSON corrupto
 
def save_inventory(items):
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(items, f)
 
def add_item(name, qty, price):
    items = load_inventory()
    items.append({'name': name, 'qty': qty, 'price': price})
    save_inventory(items)  # ⚠ acepta qty y price negativos
 
def update_price(name, new_price):
    items = load_inventory()
    for item in items:
        if item['name'] == name:
            item['price'] = new_price  # ⚠ sin validar new_price
    save_inventory(items)
 
def get_total_value():
    return sum(i['qty'] * i['price'] for i in load_inventory())
