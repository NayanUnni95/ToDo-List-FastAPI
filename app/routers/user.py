"""
This module defines the user-related API endpoints for the FastAPI application.
"""

from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from ..schema import schemas
from ..database import config

from ..services.Oauth2 import get_current_user
from ..repository import user


router = APIRouter(tags=["User"])
refresh_token_schema = HTTPBearer()

"""
- POST /signup: Endpoint for user registration.
"""


@router.post("/signup", status_code=201)
async def signup(request: schemas.UserSignup, session: config.SessionDep):
    return user.signup_user(request, session)


"""
- POST /login: Endpoint for user login and authentication.
"""


@router.post("/login")
async def login(
    session: config.SessionDep,
    request: OAuth2PasswordRequestForm = Depends(),
):
    return user.login_user(request, session)


"""
- POST /refresh: Endpoint for retrieve the currently authenticated user details.
"""


@router.post("/refresh")
def get_token(
    session: config.SessionDep,
    token_data: HTTPBearer = Depends(refresh_token_schema),
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return user.get_tokens(session, token_data)


"""
- DELETE /remove: Endpoint for deleting the currently authenticated user.
"""


@router.delete("/remove")
async def delete(
    session: config.SessionDep,
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return await user.delete_user(session, get_current_user)
