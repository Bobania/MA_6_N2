import enum
from pydantic import BaseModel
from typing_extensions import List, Optional
from sqlalchemy import DateTime, Enum


class ProductStatuses(enum.Enum):
    DELIVERY = "delivery"
    AVAILABLE = "available"
    NEED_DELIVERY = "need_delivery"
    STOP_SALES = "stop_sales"


class ProductIn(BaseModel):
    name: str
    description: str
    in_stock: int
    price_rub: int
    status: ProductStatuses


class ProductOut(ProductIn):
    id: int
