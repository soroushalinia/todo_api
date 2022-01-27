from datetime import datetime
from pydantic import BaseModel
from typing import List


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
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    todos: List[Todo] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
