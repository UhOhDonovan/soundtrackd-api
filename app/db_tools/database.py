from sqlmodel import Session, create_engine
from fastapi import Depends
from typing import Annotated
from ..dependencies.constants import SQLALCHEMY_DATABASE_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
