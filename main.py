from typing import Union
from fastapi import FastAPI, HTTPException
import uvicorn
import mysql.connector

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello", "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# Register for an account. SQL part works, not necessarily the response part
@app.post("/register/")
def create(email: str, username: str, password: str):
    global db, cursor
    print("Recieved registration request from", email, username, password)
    # Check for nonunique email -- this doesn't quite work right I don't think
    cursor.execute("SELECT email FROM user")
    result = [i[0] for i in cursor.fetchall()]
    if email in result:
        raise HTTPException(status_code=400, detail="A user exists with this email")

    # Check for nonunique username -- this doesn't quite work right I don't think
    cursor.execute("SELECT username FROM user")
    result = [i[0] for i in cursor.fetchall()]
    if username in result:
        raise HTTPException(status_code=400, detail="A user exists with this username.")

    cursor.execute(
        f"INSERT INTO user VALUES ('{email}', '{username}', '{password}', '{username}')"
    )
    db.commit()
    return {"email": email, "username": username, "password": password}


if __name__ == "__main__":
    # Decide whether to use MySql features or start the server without
    if input("Connect to MySql? (y/n): ") == "y":
        mysql_user = input("Enter MySQL username (usually root): ")
        mysql_password = input("Enter MySQL password: ")
        try:
            db = mysql.connector.connect(
                host="localhost",
                user=mysql_user,
                passwd=mysql_password,
                database="soundtrackd",
            )
            cursor = db.cursor()
        except:
            print(
                "There was an error. Retry your MySQL username/password and make sure you have a database named 'soundtrackd'."
            )

    uvicorn.run(app, port=5345)
