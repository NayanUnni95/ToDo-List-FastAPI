from fastapi import Depends
from sqlalchemy.orm import Session
from ..schema import schemas
from ..model import models
from ..database import config
from ..services.hashing import Hash
from ..services.jwtToken import create_access_token
from ..services.Oauth2 import get_current_user


def signup_user(request, db):
    users = db.query(models.Users).filter(models.Users.uname == request.uname).first()
    if users:
        return schemas.InvalidInput(
            description="That username is unavailable :( please try a different one.",
            status_code=404,
        )
    new_user = models.Users(
        name=request.name,
        uname=request.uname,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return schemas.SignupRes(
        id=new_user.id,
        name=new_user.name,
        uname=new_user.uname,
        message="User registered successfully :)",
    )


def login_user(request: schemas.UserLogin, db):
    user = db.query(models.Users).filter(models.Users.uname == request.username).first()
    print(user)
    if not user:
        return schemas.InvalidInput(description="Invalid Credentials", status_code=404)
    if not Hash.validate(request.password, user.password):
        return schemas.InvalidInput(description="Incorrect Password", status_code=404)
    access_token = create_access_token(data={"uname": user.uname})
    return schemas.Token(access_token=access_token, token_type="bearer")


async def delete_user(request, db):
    username = await get_current_user(request.access_token)
    user = db.query(models.Users).filter(models.Users.uname == username).first()
    if not user:
        # response.status_code = status.HTTP_404_NOT_FOUND
        return "User Not Found..."
    # user.delete(synchronize_session=False)
    # db.commit()
    return  user
    # return f"User deleted with Data: {user}"
