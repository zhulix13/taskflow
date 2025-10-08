# main.py
from fastapi import FastAPI
from database import engine, Base
import models
from routers import tasks, users, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
