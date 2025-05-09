from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from ..services.jwtToken import oauth2_scheme, SECRET_KEY, ALGORITHM
from ..database import config
from ..model import models


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(config.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username = payload.get("uname")
        user = db.query(models.Users).filter(models.Users.uname == username).first()
        if not user:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user
