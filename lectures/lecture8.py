from fastapi import FastAPI,Form
from pydantic import BaseModel, Field, HttpUrl
from typing import List
from uuid import UUID
from datetime import date, datetime, time, timedelta



app = FastAPI()
class Event(BaseModel):
    event_id: UUID
    start_date: date
    start_time: datetime
    end_time: datetime
    repeat_time: time 
    execute_after: timedelta

@app.post('/addevent')
def addevent(event: Event):
    return event


@app.post('/login')
def addform(username: str = Form(...), password: str = Form(...)):
    return {'username': username, 'password': password}

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

