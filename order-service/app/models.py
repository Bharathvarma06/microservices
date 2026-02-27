from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.database import Base

class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    product_id = Column(Integer)
    quantity = Column(Integer)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    total_amount = Column(Float)
    status = Column(String(50), default="CREATED")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer)
    quantity = Column(Integer)
    price = Column(Float)
