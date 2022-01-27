from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from crud import user_crud
from database import get_db
from auth import create_token
import schemas


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = user_crud.verify_user(
        db=db, email=form_data.username.lower(), password=form_data.password)

    email = form_data.username
    token = create_token(
        username=email, id=user.id)

    return {"access_token": token, "token_type": "bearer"}
