from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import UUID4
from ..schema import schemas
from ..model import models
from ..database import config
from ..utils.hashing import Hash
from ..utils.jwtToken import create_access_token
from ..utils.Oauth2 import get_current_user


router = APIRouter(tags=["/user"])


@router.post("/signup", status_code=201)
async def signup(request: schemas.UserSignup, db: Session = Depends(config.get_db)):
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


@router.post("/login")
async def login(request: schemas.UserLogin, db: Session = Depends(config.get_db)):
    user = db.query(models.Users).filter(models.Users.uname == request.uname).first()
    print(user)
    if not user:
        return schemas.InvalidInput(description="Invalid Credentials", status_code=404)
    if not Hash.validate(request.password, user.password):
        return schemas.InvalidInput(description="Incorrect Password", status_code=404)
    access_token = create_access_token(data={"uname": user.uname})
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.delete("/remove")
async def delete(
    db: Session = Depends(config.get_db),
    get_current_user: schemas.UserLogin = Depends(get_current_user),
):
    pass
