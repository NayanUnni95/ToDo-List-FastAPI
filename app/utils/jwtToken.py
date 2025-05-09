from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from decouple import config

SECRET_KEY: str = config("SECRET_KEY", default="")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
    config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
