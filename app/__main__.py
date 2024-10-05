from fastapi import FastAPI
import uvicorn
import mysql.connector
from .dependencies.colors import RED, BOLD, END, WELCOME_MSG

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello", "World"}

if __name__ == "__main__":
    # Decide whether to use MySql features or start the server without
    use_online = input(
        "Would you like to use the hosted database for Soundtrackd? (enter y if yes): "
    )
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
            print(RED + BOLD + "oops, couldn't connect to database. That's weird" + END)
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
