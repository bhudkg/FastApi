from fastapi import APIRouter, Depends, status, HTTPException

from ..schemas import Login
from .. import database, models
from fastapi.security import OAuth2PasswordBearer
from ..schemas import TokenData
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..database import get_db
import hashlib
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

SECRET_KEY = "76e3df2937aba2a670c227c249664ccbcc5bff8dd4512fa6f91a3349dbd78b48"
ALGORITHM = "HS356"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, alogrithm=ALGORITHM)
    return encoded_jwt

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Seller).filter(models.Seller.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Username not found")
    input_hash = hashlib.sha256(request.price.encode()).hexdigest()
    if input_hash != user.price:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    ## gen jwt tokens
    access_token = generate_token(data = {"sub": user.username})
    

    
    
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid auth credentials",
        headers={'WWW-Authenticate': "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username:
            token_data = TokenData(username=username)
        else:
            raise credentials_exception
    except JWTError:
        raise credentials_exception 



