from sqlalchemy import Column, Integer, String, Boolean, Float
from database import Base

class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    cat = Column(String)
    badge = Column(String, nullable=True)
    description = Column(String, nullable=True)
    img = Column(String)
    active = Column(Boolean, default=True)

class CategoryDB(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
