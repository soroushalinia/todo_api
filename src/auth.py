from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from database import get_db


SECRET_KEY = "debccf0bbd292c2fee86a80d0de0da24ae024af47e2abd5717070b5331f54fb8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_token(username: str, id: int):
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    token_data = {"id": id, "sub": username, "exp": expire_time}

    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)


def get_auth_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        id = payload.get("id")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = {"email": email, "id": id}

    return user
