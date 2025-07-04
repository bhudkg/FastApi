from fastapi import FastAPI
from pydantic import BaseModel, Field, HttpUrl
from typing import List

#Sample data
app = FastAPI()

class Image(BaseModel):
    name: HttpUrl 
    url : str
class Product(BaseModel):
    name: str = Field(examples="phone")
    price: int = Field(title="This is price", description="this would be price tag", gt=10)
    discount: int 
    discounted_price: float 
    tags: List[str] = Field(examples="[electronics, Phone]")
    image: List[Image]

    # class Config:
    #     json_schema_extra={
    #        "example": {
    #             "name": "phone",
    #         "price": 100,
    #         "discount": 10,
    #         "discounted_price": 0,
    #         "tags": ["electroices", "Computers"],
    #         "image": [
    #             {"url": "https://www.google.com", "name": "phone_image"},
    #             {"url": "https://www.facebook.com", "name": "laptop_image"}
    #         ]
    #        }
    #     }

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

