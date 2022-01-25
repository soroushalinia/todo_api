from datetime import datetime
from pydantic import BaseModel


class TodoBase(BaseModel):
    task_name: str


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    task_done: bool


class Todo(TodoBase):
    id: int
    task_done: bool
    task_date: datetime

    class Config:
        orm_mode = True
