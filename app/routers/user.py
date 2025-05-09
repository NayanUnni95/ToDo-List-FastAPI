from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..schema import schemas
from ..database import config
from ..services.Oauth2 import get_current_user
from ..repository import user


router = APIRouter(tags=["User"])


@router.post("/signup", status_code=201)
async def signup(request: schemas.UserSignup, db: Session = Depends(config.get_db)):
    return user.signup_user(request, db)


@router.post("/login")
async def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(config.get_db)
):
    return user.login_user(request, db)


@router.delete("/remove")
async def delete(
    db: Session = Depends(config.get_db),
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return await user.delete_user(db, get_current_user)
