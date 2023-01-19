from pydantic import BaseModel
from datetime import datetime


class Product(BaseModel):
    key: str
    code: int
    codebar: str
    codebarInner: str
    codebarMaster: str
    unit: str
    description: str
    brand: str
    buy: float
    retailsale: float
    wholesale: float
    inventory: int
    min_inventory: int
    department: str
    id: int
    LastUpdate: datetime