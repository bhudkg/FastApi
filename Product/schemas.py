from pydantic import BaseModel
from typing import Optional
from .models import Product

class Product(BaseModel):
    name: str 
    description: str 
    price: int 
    seller_id: Optional[int] = None

# display products
class DisplayProduct(BaseModel):
    id: int
    name: str 
    description: str
    price: int
    seller_id: Optional[int] = None

    class Config:
        orm_mode = True

# seller
class Seller(BaseModel):
    username: str
    email: str 
    price: str 

class Login(BaseModel):
    username: str 
    price: str 


class Token(BaseModel):
    access_token: str 
    token_type: str 

class TokenData(BaseModel):
    username : Optional[str] = None

