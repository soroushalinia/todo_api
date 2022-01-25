from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy import schema
from sqlalchemy.orm import Session

from crud import user_crud
import schemas
from database import get_db

router = APIRouter(tags=["User"])


@router.get('/user/{id}', response_model=schemas.User, description="Get user by id.")
def get_user(id: int = Path(..., ge=0), db: Session = Depends(get_db)):
    user = user_crud.get_user_by_id(db=db, id=id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exists.")
    else:
        return user


@router.post("/user", response_model=schemas.User, status_code=status.HTTP_201_CREATED, description="Creates a user.")
def create_user(todo: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db=db, request=todo)
