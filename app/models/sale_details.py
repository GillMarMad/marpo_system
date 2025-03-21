
# from app.models.products import Product
# from app.models.sale import Sale
from db.base_class import Base
from sqlalchemy import Column, DateTime,Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
# from sqlalchemy.orm import relationship
from datetime import datetime



class SalesDetail(Base):
    __tablename__ = 'sales_details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sale_id = Column(Integer, ForeignKey('sales.id', ondelete='RESTRICT'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='RESTRICT'), nullable=False)
    quantity = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)
    buy_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    sale = relationship("Sale", back_populates="sales_details")
    product = relationship("Product", back_populates="sales_details")