# main.py
from fastapi import FastAPI
from database import engine, Base
import models
from routers import tasks, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")

app.include_router(tasks.router)
app.include_router(users.router)
