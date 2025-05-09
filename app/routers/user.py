from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schema import schemas
from ..model import models
from ..database import config
from ..utils.hashing import Hash


router = APIRouter(tags=["/user"])


@router.post("/signup", status_code=201)
async def signup(request: schemas.UserSignup, db: Session = Depends(config.get_db)):
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
        message="User registered successfully",
    )
