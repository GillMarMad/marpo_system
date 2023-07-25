from pydantic import BaseModel
from datetime import datetime

class Sell(BaseModel):
    id: int
    id_sell: int
    id_product: str
    amount: float
    sell_price: float
    buy_price: float
    total: float
    date: datetime


class SellProduct(BaseModel):
    key : str
    retail : bool
    amount : int