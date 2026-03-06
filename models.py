from enum import Enum
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Enum as SQLEnum,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PrintType(str, Enum):
    BW = "B&W"
    COLORED = "Colored"
    PHOTO_PAPER = "Photo Paper"


class OrderStatus(str, Enum):
    PENDING = "Pending"
    PAID = "Paid"
    COMPLETED = "Completed"


class OrderDB(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, nullable=False)
    document_name = Column(String, nullable=False)
    pages = Column(Integer, nullable=False)
    print_type = Column(SQLEnum(PrintType), nullable=False)
    total_cost = Column(Float, nullable=False)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING)


# Pydantic schemas used for request/response validation
class OrderCreate(BaseModel):
    student_name: str
    document_name: str
    pages: int
    print_type: PrintType


class OrderUpdate(BaseModel):
    student_name: Optional[str] = None
    document_name: Optional[str] = None
    pages: Optional[int] = None
    print_type: Optional[PrintType] = None
    status: Optional[OrderStatus] = None


class OrderResponse(OrderCreate):
    order_id: int
    total_cost: float
    status: OrderStatus

    class Config:
        orm_mode = True


class Payment(BaseModel):
    amount: float