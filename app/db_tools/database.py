from sqlmodel import Session, create_engine
from fastapi import Depends
from typing import Annotated
import os

user = "root"
# TODO: Store password as a secret
password = "password"
host = "0.0.0.0"
port = 3306
database = "soundtrackd"
container_name = "soundtrackd-db"

if "IS_CONTAINER" in os.environ:
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{0}:{1}@{2}/{3}".format(
        user, password, container_name, database
    )
else:
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
        user, password, host, port, database
    )


engine = create_engine(SQLALCHEMY_DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
