from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import models
import schemas


def get_all_todos(db: Session):
    return db.query(models.Todo).all()


def get_todo(db: Session, id: int):
    return db.query(models.Todo).filter(models.Todo.id == id).first()


def create_todo(db: Session, request: schemas.TodoCreate):
    todo = models.Todo(task_name=request.task_name,
                       task_date=datetime.utcnow())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def update_todo(db: Session, id: int, request: schemas.TodoUpdate):
    todo = db.query(models.Todo).filter(models.Todo.id == id)
    if not todo.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task does not exist.")
    else:
        todo.update({"task_name": request.task_name,
                    "task_done": request.task_done})
        db.commit()
        return todo.first()


def delete_todo(db: Session, id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == id)
    if not todo.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task does not exist.")
    else:
        todo.delete(synchronize_session=False)
        db.commit()
        return "Task Deleted."