import json
import os
from typing import List
from models import Order

DATA_FILE = "orders.json"

def load_orders() -> List[Order]:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return [Order(**item) for item in data]
    return []

def save_orders(orders: List[Order]):
    with open(DATA_FILE, "w") as f:
        json.dump([order.dict() for order in orders], f, indent=4)

# In-memory storage
orders_db: List[Order] = load_orders()

def get_next_order_id() -> int:
    if orders_db:
        return max(order.order_id for order in orders_db if order.order_id) + 1
    return 1