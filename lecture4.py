from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Set 

app = FastAPI()

#request body with path parameter and queryparameter

class Product(BaseModel):
    name: str
    price: int = Field(title="Price of the item", description="This would be the price of the item", gt=1)
    discount: int 
    discounted_price : float 
    tags: Set[str]  = []


class User(BaseModel):
    name: str
    email: str 

@app.post('/purchase')
def purchase(user: User, product: Product):
    return {'user': User, 'product': Product}


@app.post('/addproduct/{id}')
def addproduct(product: Product, id:int, category: str):
    product.discounted_price = product.price - (product.price * product.discount)/100
    return {'id': id, "product": product, "category": category}




#Body fields 





