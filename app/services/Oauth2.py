"""
This module provides the `get_current_user` function for authenticating and retrieving
the current user based on a JWT token.
"""

from fastapi import Depends, HTTPException, status
from sqlmodel import select
from jose import jwt, JWTError
from ..services.jwtToken import oauth2_scheme, SECRET_KEY, ALGORITHM
from ..database.config import SessionDep
from ..model import models

"""
Validates the provided JWT token, decodes it to extract the username, and retrieves
the corresponding user from the database. Raises an HTTPException if the token is
invalid or the user does not exist.
"""

# Get the user details


async def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(session, token, credentials_exception)


# Verify the token expire or not


def verify_token(session, token, credentials_exception: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username = payload.get("uname")
        statement = select(models.Users).where(models.Users.uname == username)
        user = session.exec(statement).first()
        if not user:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user
