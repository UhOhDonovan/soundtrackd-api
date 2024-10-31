from fastapi import FastAPI
import uvicorn
from .dependencies.colors import WELCOME_MSG
from .db_tools.models import SQLModel
from .db_tools.database import SessionDep
from .routes import users
from sqlalchemy import text

app = FastAPI()

app.include_router(users.router, prefix="/users")


@app.get("/")
def read_root(session: SessionDep):  # Table check
    model_tables = set(SQLModel.metadata.tables.keys())

    tables = session.exec(
        text(
            f"SELECT table_name FROM information_schema.tables WHERE table_schema = 'soundtrackd'"
        )
    )
    db_tables = {row[0] for row in tables}

    missing_tables = model_tables - db_tables
    if missing_tables:
        return ("Missing tables in the database:", missing_tables)
    return "All tables are present in the database."


if __name__ == "__main__":
    print("\n" + WELCOME_MSG + "\n")
    uvicorn.run(app, host="0.0.0.0", port=5345)
