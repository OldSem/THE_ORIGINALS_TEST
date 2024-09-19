from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
# from . import models, schemas, auth
from config.database import SessionLocal, engine

from base.models import Base
from auth import routers as auth_routers
from task import routers as tasks_routers

app = FastAPI()


app.include_router(auth_routers.router)
app.include_router(tasks_routers.router)


@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI!"}




