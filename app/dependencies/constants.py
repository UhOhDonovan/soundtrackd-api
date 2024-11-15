import os

from dotenv import main

main.load_dotenv()

# OAuth2 authentication
SECRET_KEY = os.getenv("API_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database authentication
DB_USER = "root"
DB_PASSWORD = os.getenv("DB_PASSWORD")
HOST = "0.0.0.0"
PORT = 3306
DATABASE = "soundtrackd"
CONTAINER_NAME = "soundtrackd-db"

if "IS_CONTAINER" in os.environ:
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{0}:{1}@{2}/{3}".format(
        DB_USER, DB_PASSWORD, CONTAINER_NAME, DATABASE
    )
else:
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
        DB_USER, DB_PASSWORD, HOST, PORT, DATABASE
    )
