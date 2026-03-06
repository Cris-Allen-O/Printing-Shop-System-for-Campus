from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from models import (
    OrderDB,
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    Payment,
    PrintType,
    OrderStatus,
)
from database import get_db

router = APIRouter()

PRICES = {
    PrintType.BW: 2.0,
    PrintType.COLORED: 5.0,
    PrintType.PHOTO_PAPER: 20.0,
}


def calculate_total_cost(pages: int, print_type: PrintType) -> float:
    return pages * PRICES[print_type]


@router.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    total = calculate_total_cost(order.pages, order.print_type)
    db_order = OrderDB(
        student_name=order.student_name,
        document_name=order.document_name,
        pages=order.pages,
        print_type=order.print_type,
        total_cost=total,
        status=OrderStatus.PENDING,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/orders", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(OrderDB).all()


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderDB).filter(OrderDB.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/orders/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int, updated_order: OrderUpdate, db: Session = Depends(get_db)
):
    order = db.query(OrderDB).filter(OrderDB.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if updated_order.student_name is not None:
        order.student_name = updated_order.student_name
    if updated_order.document_name is not None:
        order.document_name = updated_order.document_name
    if updated_order.pages is not None:
        order.pages = updated_order.pages
    if updated_order.print_type is not None:
        order.print_type = updated_order.print_type
    if updated_order.status is not None:
        order.status = updated_order.status

    order.total_cost = calculate_total_cost(order.pages, order.print_type)
    db.commit()
    db.refresh(order)
    return order


@router.post("/orders/{order_id}/pay")
def pay_order(order_id: int, payment: Payment, db: Session = Depends(get_db)):
    order = db.query(OrderDB).filter(OrderDB.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail="Order already paid or completed")
    if payment.amount < order.total_cost:
        raise HTTPException(status_code=400, detail="Insufficient payment")
    change = payment.amount - order.total_cost
    order.status = OrderStatus.PAID
    db.commit()
    return {"message": "Payment successful", "change": change}


@router.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderDB).filter(OrderDB.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted"}