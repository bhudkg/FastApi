from fastapi import APIRouter
from .. import schemas, models
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from fastapi import FastAPI, Response, status, HTTPException
from Product.routers.login import get_current_user


router = APIRouter()


@router.post('/product')
def add(request: schemas.Product, db: Session = Depends(get_db), current_user: schemas.Seller = Depends(get_current_user)):
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
@router.get('/products', response_model=List[schemas.DisplayProduct])
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

# get product based on the id
@router.get('/product/{id}', response_model=schemas.DisplayProduct)
def product(id, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

# to delete the product
@router.delete('/product/{id}')
def delete(id, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {"message": "Product deleted successfully"}

# update the product
@router.put('/product/{id}')
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