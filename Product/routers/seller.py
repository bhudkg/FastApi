from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from ..import schemas
from .. import models
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
import hashlib

router = APIRouter()


@router.post('/seller')
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    # Hash the password using SHA-256 instead of bcrypt to avoid the version issue
    hash_password = hashlib.sha256(request.price.encode()).hexdigest()
    new_seller = models.Seller(username=request.username, email=request.email, price=hash_password)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return {"message": "Seller created successfully", "username": request.username} 