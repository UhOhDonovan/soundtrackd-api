from typing import Union, Annotated
from fastapi import HTTPException, Response, APIRouter, Query
from ..dependencies.apimodels import RegistrationObject
from sqlmodel import select
from ..db_tools.models import User
from ..db_tools.database import SessionDep
import getpass
import re
import hashlib

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
def register_user(session: SessionDep, new_user: RegistrationObject):
    hashed_password = hashlib.sha256(new_user.password.encode()).hexdigest()

    user = User(
        email=new_user.email, username=new_user.username, password=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user