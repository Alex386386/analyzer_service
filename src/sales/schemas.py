from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SalesBase(BaseModel):
    product_id: int
    name: str
    quantity: int
    price: float
    category: str


class SalesUpdate(SalesBase):
    product_id: Optional[int] = None
    name: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    category: Optional[str] = None


class SalesCreate(SalesBase):
    pass


class SalesDB(SalesBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_date: datetime
    update_date: datetime
