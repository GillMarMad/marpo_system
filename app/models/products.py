from db.base_class import Base
from sqlalchemy import Boolean, Column, String, DateTime,Integer, Float
from datetime import datetime

class Product(Base):
    key = Column(String, primary_key=True,
                index=True, nullable=False)
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
    id = Column(Integer, unique=False, nullable=True)
    box = Column(Integer, default=0)
    master = Column(Integer, default=0)
    lastupdate = Column(DateTime, default=datetime.now())