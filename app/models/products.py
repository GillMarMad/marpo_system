from db.base_class import Base
from sqlalchemy import Boolean, Column, String, DateTime,Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.sale import sales_products
from datetime import datetime

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, unique=False, nullable=False, autoincrement=True, primary_key=True, index=True)
    key = Column(String, index=True, nullable=False)
    code = Column(String, unique=True, nullable=True)
    codebar = Column(String, unique=True, nullable=True)
    codebarinner = Column(String, unique=True, nullable=True)
    codebarmaster = Column(String, unique=True, nullable=True)
    unit = Column(String, nullable=False)
    description = Column(String, nullable=False)
    brand = Column(String, nullable=True)
    buy = Column(Float, nullable=False)
    retailsale = Column(Float, nullable=False)
    wholesale = Column(Float, nullable=False)
    inventory = Column(Integer, nullable=True)
    min_inventory = Column(Integer, nullable=True)
    department = Column(String, nullable=True)
    origin_id = Column(Integer, nullable=True)
    box = Column(Integer, default=0)
    master = Column(Integer, default=0)
    lastupdate = Column(DateTime, default=datetime.now())
    sales = relationship('Sale', secondary=sales_products, back_populates='products')