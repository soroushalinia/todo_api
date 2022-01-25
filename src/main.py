from fastapi import FastAPI
from database import engine
import models
from routes import todo_route

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(todo_route.router)
