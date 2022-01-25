from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List

from crud import todo_crud
import schemas
from database import get_db


router = APIRouter(tags=["Todo"])


@router.get("/todos/{user_id}", response_model=List[schemas.Todo], description="Gets all of created tasks from database for a specific user.")
def get_todos(user_id: int = Path(..., ge=0), db: Session = Depends(get_db)):
    return todo_crud.get_all_todos(db=db, user_id=user_id)


@router.get("/todo/{id}", response_model=schemas.Todo, description="Gets a task by id.")
def get_todo_by_id(id: int = Path(..., ge=0), db: Session = Depends(get_db)):
    todo = todo_crud.get_todo(db=db, id=id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task does not exist.")
    else:
        return todo


@router.post("/todo", response_model=schemas.Todo, status_code=status.HTTP_201_CREATED, description="Creates a new task.")
def post_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return todo_crud.create_todo(db=db, request=todo)


@router.put("/todo/{id}", response_model=schemas.Todo, description="Updates a task by id.")
def update_todo(todo: schemas.TodoUpdate, id: int = Path(..., ge=0), db: Session = Depends(get_db)):
    return todo_crud.update_todo(db=db, request=todo, id=id)


@router.delete("/todo/{id}", description="Deletes a task by id.")
def delete_todo(id: int = Path(..., ge=0), db: Session = Depends(get_db)):
    return todo_crud.delete_todo(id=id, db=db)
