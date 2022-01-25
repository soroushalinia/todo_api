from fastapi import FastAPI
from database import engine
import models
from routes import todo_route, user_route

tags_metadata = [
    {
        "name": "Todo",
        "description": "CRUD pperations for tasks.",
    },
    {
        "name": "User",
        "description": "User related routes."
    }
]

models.Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_tags=tags_metadata,
              title="Todo API", description="Simple Todo api written using FastAPI", license_info={
                  "name": "MIT",
                  "url": "https://mit-license.org/"
              })

app.include_router(todo_route.router)
app.include_router(user_route.router)
