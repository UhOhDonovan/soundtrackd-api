from typing import Union
from fastapi import FastAPI, HTTPException, Response
import uvicorn
import mysql.connector
from pydantic import BaseModel
import getpass
import re
import hashlib

END = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"
UNDERSCORE = "\033[4m"
BLINK = "\033[5m"
REVERSE = "\033[7m"
HIDDEN = "\033[7m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

END = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"
UNDERSCORE = "\033[4m"
BLINK = "\033[5m"
REVERSE = "\033[7m"
HIDDEN = "\033[7m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
WELCOME_MSG = (
    BOLD
    + GREEN
    + """  /$$$$$$   /$$$$$$  /$$   /$$ /$$   /$$ /$$$$$$$  /$$$$$$$$ /$$$$$$$   /$$$$$$   /$$$$$$  /$$   /$$ /$$$$$$$ 
 /$$__  $$ /$$__  $$| $$  | $$| $$$ | $$| $$__  $$|__  $$__/| $$__  $$ /$$__  $$ /$$__  $$| $$  /$$/| $$__  $$
| $$  \__/| $$  \ $$| $$  | $$| $$$$| $$| $$  \ $$   | $$   | $$  \ $$| $$  \ $$| $$  \__/| $$ /$$/ | $$  \ $$
|  $$$$$$ | $$  | $$| $$  | $$| $$ $$ $$| $$  | $$   | $$   | $$$$$$$/| $$$$$$$$| $$      | $$$$$/  | $$  | $$
 \____  $$| $$  | $$| $$  | $$| $$  $$$$| $$  | $$   | $$   | $$__  $$| $$__  $$| $$      | $$  $$  | $$  | $$
 /$$  \ $$| $$  | $$| $$  | $$| $$\  $$$| $$  | $$   | $$   | $$  \ $$| $$  | $$| $$    $$| $$\  $$ | $$  | $$
|  $$$$$$/|  $$$$$$/|  $$$$$$/| $$ \  $$| $$$$$$$/   | $$   | $$  | $$| $$  | $$|  $$$$$$/| $$ \  $$| $$$$$$$/
 \______/  \______/  \______/ |__/  \__/|_______/    |__/   |__/  |__/|__/  |__/ \______/ |__/  \__/|_______/ """
    + END
)
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello", "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


class Register(BaseModel):
    email: str
    username: str
    password: str


# Register for an account. SQL part works, not necessarily the response part
@app.post("/register")
def create(info: Register):
    global db, cursor
    valid_email = re.compile(r"^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    whitespace = re.compile(r"\w")
    # Check for nonunique email and username
    cursor.execute("SELECT email, username FROM user")
    taken_users = cursor.fetchall()
    for user in taken_users:
        if valid_email.match(info.email):
            if info.email == user[0]:
                raise HTTPException(
                    status_code=400, detail="A user exists with this email"
                )
            if info.username == user[1]:
                raise HTTPException(
                    status_code=400, detail="A user exists with this username"
                )

    if len(info.password) < 4:
        raise HTTPException(status_code=400, detail="Password is too short")
    elif (
        (" " in info.password)
        or ("\t" in info.password)
        or ("\n" in info.password)
        or ("\r" in info.password)
    ):
        raise HTTPException(status_code=400, detail="Your password contains whitespace")

    password = hashlib.sha256(info.password.encode()).hexdigest()

    cursor.execute(
        f"INSERT INTO user VALUES ('{info.email}', '{info.username}', '{password}')"
    )
    db.commit()
    return {
        "email": info.email,
        "username": info.username,
        "message": "Registered successfully!",
    }


class Login(BaseModel):
    user_field: str
    password: str


@app.post("/login")
def login(info: Login, response: Response):
    global cursor
    done = False
    key = "username"
    valid_email = re.compile(r"^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    if valid_email.match(info.user_field):
        cursor.execute(
            "SELECT username, password FROM user WHERE email = %s", [info.user_field]
        )
        key = "email"
    else:
        cursor.execute(
            "SELECT username, password FROM user WHERE username = %s",
            [info.user_field],
        )

    db_result = cursor.fetchall()
    if db_result:
        for result in db_result:
            if result[0] == info.user_field:
                if result[1] == hashlib.sha256(info.password.encode()).hexdigest():
                    response.set_cookie(key=key, value=info.user_field)
                    return {"message": "login successful"}
                return {"message": "invalid username/password"}
    return {"message": "user not found"}


if __name__ == "__main__":
    # Decide whether to use MySql features or start the server without
    use_online = input("Would you like to use the hosted database for Soundtrackd? (enter y if yes): ")
    if use_online == "y":
        try:
            pswd = input("Enter the password for the online database: ")
            timeout = 10
            db = mysql.connector.connect(
                host="soundtrackd-mysql-soundtrackd.d.aivencloud.com",
                port=27106,
                user="avnadmin",
                passwd=pswd,
                database="defaultdb",
            )
            cursor = db.cursor()
        except:
            print(
                RED
                + BOLD
                + "oops, couldn't connect to database. That's weird"
                + END
            )
    else:
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

    print("\n" + WELCOME_MSG + "\n")
    uvicorn.run(app, port=5345)
