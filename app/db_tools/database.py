from sqlmodel import Field, Session, SQLModel, create_engine
from .models import User

user = "root"
# TODO: Store password as a secret
password = "password"
host = "127.0.0.1"
port = 3306
database = "soundtrackd"

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
    user, password, host, port, database
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session
