from typing import Union, Annotated
from fastapi import HTTPException, Response, APIRouter, Query
from dependencies.apimodels import RegistrationObject
from sqlmodel import select
from db_tools.models import User
from db_tools.database import SessionDep
from requests import post, get
import base64
import json
import getpass
import re
import hashlib

router = APIRouter()

CLIENT_ID = "82f96e6cf1814f488b6d664ffc0d7587"
CLIENT_SECRET = "14e72310fc734968b4a6d3d74a26a2d9"


def get_token() -> str:
    """Retrieve access token for Spotify API (expires after 1 hour)"""
    authorization_str = (CLIENT_ID + ":" + CLIENT_SECRET).encode("utf-8")
    authorization_str = str(base64.b64encode(authorization_str), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + authorization_str,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    response = post(url, headers=headers, data=data)
    token = json.loads(response.content)["access_token"]
    return token


@router.get("/album")
def search_album(q: str):
    type = "album"
    token = get_token()
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": "Bearer " + token}
    query = f"?q={q}&type={type}&limit=10"
    query_url = url + query
    response = get(query_url, headers=headers)
    result = json.loads(response.content)[type + "s"]["items"]
    print(result)
    return result


@router.get("/artist")
def search_artist(q: str):
    type = "artist"
    token = get_token()
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": "Bearer " + token}
    query = f"?q={q}&type={type}&limit=10"
    query_url = url + query
    response = get(query_url, headers=headers)
    result = json.loads(response.content)[type + "s"]["items"]
    print(result)
    return result


# @router.get("/list")
# def get_users(
#     session: SessionDep,
#     offset: int = 0,
#     limit: Annotated[int, Query(le=100)] = 100,
# ):
#     users = session.exec(select(User).offset(offset).limit(limit)).all()
#     return users


# @router.post("/register")
# def register_user(session: SessionDep, new_user: RegistrationObject):
#     hashed_password = hashlib.sha256(new_user.password.encode()).hexdigest()

#     user = User(
#         email=new_user.email, username=new_user.username, password=hashed_password
#     )

#     session.add(user)
#     session.commit()
#     session.refresh(user)

#     return user
