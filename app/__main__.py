from fastapi import FastAPI, Depends
from typing import Annotated
import uvicorn
from .dependencies.colors import WELCOME_MSG
from .db_tools.models import User
from .db_tools.database import get_session, Session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello", "World"}

if __name__ == "__main__":
    print("\n" + WELCOME_MSG + "\n")
    uvicorn.run(app, port=5345)
