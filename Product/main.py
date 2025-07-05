from fastapi import FastAPI, Response, status, HTTPException
from .import schemas
from . import models
from .database import engine, SessionLocal
from .routers import product, seller, login

app = FastAPI()

# making a session of the db
app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)
# Then recreate them based on current models
models.Base.metadata.create_all(bind=engine)

#
