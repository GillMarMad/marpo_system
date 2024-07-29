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