from pydantic import BaseModel
from datetime import datetime

class Sale(BaseModel):
    product_id: int
    quantity: float
    sell_price: float

class SaleSchema(BaseModel):
    id: int
    seller: str
    costumer: str
    total: float
    products: list[Sale]

class SaleDetail(BaseModel):
    id : int
    sale_id: int
    product_id: int
    quantity: float
    total_price: float
    created_at: datetime
    updated_at: datetime
    sell_price: float
    buy_price: float