from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


# database model
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    seller_id = Column(Integer, ForeignKey('seller.id'))
    seller = relationship('Seller', back_populates='products')


class Seller(Base):
    __tablename__ = 'seller'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    price = Column(String)
    products = relationship('Product', back_populates='seller') 