from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
from hash import hash_password


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).get(id)


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, request: schemas.UserCreate):
    if not get_user_by_email(db=db, email=request.email):
        hashed_password = hash_password(request.password)
        user = models.User(email=request.email, password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_200_OK, detail=f"User with email '{request.email}' exists.")
