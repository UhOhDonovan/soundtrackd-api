from typing import Union, Annotated
from fastapi import HTTPException, Response, APIRouter, Query, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ..dependencies.apimodels import RegistrationObject
from ..dependencies.authentication import get_current_user, create_access_token
from sqlmodel import select
from ..db_tools.models import User
from ..db_tools.database import SessionDep
import getpass
import re
import hashlib
from sqlalchemy import text

router = APIRouter()

@router.get("/list")
def get_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.post("/register")
async def register_user(session: SessionDep, new_user: RegistrationObject):
    
    # Ensure we are not registeringan account with a duplicate username
    if session.query(User).filter(User.email == new_user.username).first():
        raise HTTPException(
            status_code=409,
            detail="A user already exists with this username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Ensure we are not registering an account with a duplicate email
    if session.query(User).filter(User.email == new_user.email).first():
        raise HTTPException(
            status_code=409,
            detail="A user already exists with this email",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    hashed_password = hashlib.sha256(new_user.password.encode()).hexdigest()
    user = session.get(User, new_user.username)

    if user:
        raise HTTPException(status_code=401, detail="User already exists")
    
    user = User(
        email=new_user.email, username=new_user.username, password=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.post("/token")
async def user_login(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = session.get(User, form_data.username)
    if user:
        hashed_password = hashlib.sha256(form_data.password.encode()).hexdigest()
        if user.password == hashed_password:
            access_token = create_access_token(data={"sub": user.username})
            return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=401,
        detail="Incorrect username / password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.get("/me")
async def read_users_me(current_user: Annotated[str, Depends(get_current_user)]):
    return current_user
