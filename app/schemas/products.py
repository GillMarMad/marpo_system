from pydantic import BaseModel
from datetime import datetime


class Product(BaseModel):
    id: int
    key: str
    code: str
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
    origin_id: int
    box: int
    master: int
    lastUpdate: datetime
