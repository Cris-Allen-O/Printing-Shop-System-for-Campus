from pydantic import BaseModel
from enum import Enum
from typing import Optional

class PrintType(str, Enum):
    BW = "B&W"
    COLORED = "Colored"
    PHOTO_PAPER = "Photo Paper"

class OrderStatus(str, Enum):
    PENDING = "Pending"
    PAID = "Paid"
    COMPLETED = "Completed"

class Order(BaseModel):
    order_id: Optional[int] = None
    student_name: str
    document_name: str
    pages: int
    print_type: PrintType
    total_cost: Optional[float] = None
    status: OrderStatus = OrderStatus.PENDING

class Payment(BaseModel):
    amount: float