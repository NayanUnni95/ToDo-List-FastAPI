"""
This module provides repository functions for user-related operations in a FastAPI application.
"""

from fastapi import HTTPException, status
from ..schema import schemas
from ..model import models
from ..services.hashing import Hash
from ..services.jwtToken import create_access_token

"""
signup_user(request, db):
    Registers a new user in the database. Checks for username availability and hashes the password before saving.
"""


def signup_user(request, session):
    users = (
        session.query(models.Users).filter(models.Users.uname == request.uname).first()
    )
    if users:
        raise HTTPException(
            status_code=400,
            detail="That username is unavailable :( please try a different one.",
        )
    new_user = models.Users(
        name=request.name,
        uname=request.uname,
        password=Hash.bcrypt(request.password),
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return schemas.SignupRes(
        id=new_user.id,
        name=new_user.name,
        uname=new_user.uname,
        message="User registered successfully :)",
    )


"""
login_user(request: schemas.UserLogin, db):
    Authenticates a user by validating their credentials and generates a JWT access token.
"""


def login_user(request: schemas.UserLogin, session):
    user = (
        session.query(models.Users)
        .filter(models.Users.uname == request.username)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not Hash.validate(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"uname": user.uname})
    return schemas.Token(access_token=access_token, token_type="bearer")


"""
delete_user(db, get_current_user):
    Deletes the currently authenticated user's account from the database.
"""


async def delete_user(session, get_current_user):
    user = (
        session.query(models.Users)
        .filter(models.Users.id == get_current_user.id)
        .delete(synchronize_session=False)
    )
    if user == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found...",
        )
    session.commit()
    return {"message": "Account successfully deleted."}
