from fastapi import APIRouter, HTTPException
from typing import List
from models import Order, Payment, PrintType
from database import orders_db, save_orders, get_next_order_id

router = APIRouter()

PRICES = {
    PrintType.BW: 2.0,
    PrintType.COLORED: 5.0,
    PrintType.PHOTO_PAPER: 20.0
}

def calculate_total_cost(pages: int, print_type: PrintType) -> float:
    return pages * PRICES[print_type]

@router.post("/orders", response_model=Order)
def create_order(order: Order):
    order.order_id = get_next_order_id()
    order.total_cost = calculate_total_cost(order.pages, order.print_type)
    orders_db.append(order)
    save_orders(orders_db)
    return order

@router.get("/orders", response_model=List[Order])
def get_orders():
    return orders_db

@router.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    for order in orders_db:
        if order.order_id == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")

@router.put("/orders/{order_id}", response_model=Order)
def update_order(order_id: int, updated_order: Order):
    for i, order in enumerate(orders_db):
        if order.order_id == order_id:
            updated_order.order_id = order_id
            updated_order.total_cost = calculate_total_cost(updated_order.pages, updated_order.print_type)
            orders_db[i] = updated_order
            save_orders(orders_db)
            return updated_order
    raise HTTPException(status_code=404, detail="Order not found")

@router.post("/orders/{order_id}/pay")
def pay_order(order_id: int, payment: Payment):
    for order in orders_db:
        if order.order_id == order_id:
            if order.status != "Pending":
                raise HTTPException(status_code=400, detail="Order already paid or completed")
            if payment.amount < order.total_cost:
                raise HTTPException(status_code=400, detail="Insufficient payment")
            change = payment.amount - order.total_cost
            order.status = "Paid"
            save_orders(orders_db)
            return {"message": "Payment successful", "change": change}
    raise HTTPException(status_code=404, detail="Order not found")

@router.delete("/orders/{order_id}")
def delete_order(order_id: int):
    for i, order in enumerate(orders_db):
        if order.order_id == order_id:
            del orders_db[i]
            save_orders(orders_db)
            return {"message": "Order deleted"}
    raise HTTPException(status_code=404, detail="Order not found")