from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from hash import hash_password, verify_password
import models
import schemas


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).get(id)


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email.lower()).first()


def create_user(db: Session, request: schemas.UserCreate):
    if not get_user_by_email(db=db, email=request.email.lower()):
        hashed_password = hash_password(request.password)
        user = models.User(email=request.email.lower(),
                           password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_200_OK, detail=f"User with email '{request.email}' exists.")


def verify_user(db, email: str, password: str):
    auth_error = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect Credentials.", headers={"WWW-Authenticate": "Bearer"})
    user = get_user_by_email(email=email, db=db)
    if not user:
        raise auth_error
    if not verify_password(password, user.password):
        raise auth_error
    else:
        return user
