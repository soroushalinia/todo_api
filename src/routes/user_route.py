from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas
from crud import user_crud
from database import get_db
from auth import get_auth_user

router = APIRouter(tags=["User"])


@router.get('/user', response_model=schemas.User, description="Get user by id.")
def get_user(db: Session = Depends(get_db), user=Depends(get_auth_user)):
    user = user_crud.get_user_by_id(db=db, id=user["id"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exists.")
    else:
        return user


@router.post("/user",
             response_model=schemas.User,
             status_code=status.HTTP_201_CREATED, description="Creates a user.")
def create_user(todo: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db=db, request=todo)
