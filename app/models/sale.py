# from app.models.products import Product
from db.base_class import Base
from sqlalchemy import Column, String, DateTime,Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime


class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True ,nullable=False, autoincrement=True)
    date = Column(DateTime, default=datetime.now(), nullable=False)
    seller = Column(String, nullable=False)
    costumer = Column(String, nullable=True)
    total = Column(Float, nullable=False)
    products = relationship('products')