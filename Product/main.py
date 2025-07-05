from fastapi import FastAPI, Response, status, HTTPException
from .import schemas
from . import models
from .database import engine, SessionLocal
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List
import hashlib

app = FastAPI()

# making a session of the db
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


# Then recreate them based on current models
models.Base.metadata.create_all(bind=engine)

# sending a post command to add user in the database
@app.post('/product')
def add(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name, 
        description=request.description, 
        price=request.price,
        seller_id=request.seller_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request

# get the all the products in the db
@app.get('/products', response_model=List[schemas.DisplayProduct])
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

# get product based on the id
@app.get('/product/{id}', response_model=schemas.DisplayProduct)
def product(id, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

# to delete the product
@app.delete('/product/{id}')
def delete(id, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {"message": "Product deleted successfully"}

# update the product
@app.put('/product/{id}')
def update(id, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    product.name = request.name
    product.description = request.description
    product.price = request.price
    
    db.commit()
    db.refresh(product)
    return {"message": "Product has been updated successfully"}

@app.post('/seller')
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    # Hash the password using SHA-256 instead of bcrypt to avoid the version issue
    hash_password = hashlib.sha256(request.price.encode()).hexdigest()
    new_seller = models.Seller(username=request.username, email=request.email, price=hash_password)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return {"message": "Seller created successfully", "username": request.username} 