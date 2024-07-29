from pydantic import BaseModel
from datetime import datetime

class Sale(BaseModel):
    id: int
    date: datetime
    products: str
    total: float