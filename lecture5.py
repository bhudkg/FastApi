from fastapi import FastAPI
from pydantic import BaseModel, Field, HttpUrl
from typing import List

##### Nested models 
app = FastAPI()

class Image(BaseModel):
    name: HttpUrl 
    url : str
class Product(BaseModel):
    name: str
    price: int = Field(title="This is price", description="this would be price tag", gt=10)
    discount: int 
    discounted_price: float 
    image: List[Image]

class User(BaseModel):
    name: str
    email: str 

class Offer(BaseModel):
    name: str 
    description: str
    price : float
    products: List[Product]

@app.post('/addproduct')
def addproduct(user: User, product: Product):
    return {'user':user, 'product': product}

@app.post('/addoffer')
def addoffer(offer: Offer):
    return offer

