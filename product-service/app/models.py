from sqlalchemy import Column, Integer, String, Float, Text
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(Text)
    price = Column(Float)
    stock = Column(Integer)
