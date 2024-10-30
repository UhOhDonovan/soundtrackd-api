from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    email: str = Field(unique=True)
    username: str = Field(primary_key=True)
    password: str = Field()
