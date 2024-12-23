from typing import Union, Annotated
from fastapi import HTTPException, Response, APIRouter, Query
from ..dependencies.apimodels import RegistrationObject
from sqlmodel import select
from ..db_tools.models import User
from ..db_tools.database import SessionDep
from ..dependencies.constants import SPOTIFY_ID, SPOTIFY_SECRET
from requests import post, get
import base64
import json
import getpass
import re
import hashlib
import os


router = APIRouter()


def get_token() -> str:
    """Retrieve access token for Spotify API (expires after 1 hour)"""
    authorization_str = (SPOTIFY_ID + ":" + SPOTIFY_SECRET).encode("utf-8")
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
def search_album(q: str = "test"):
    type = "album"
    token = get_token()
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": "Bearer " + token}
    query = f"?q={q}&type={type}&limit=20"
    query_url = url + query
    response = get(query_url, headers=headers)
    result = json.loads(response.content)[type + "s"]["items"]
    print(result)
    formatted_result = {"items": result}
    test = {"message": "Hello World"}
    return formatted_result


@router.get("/album/id")
def get_album(id: str = "test"):
    type = "album"
    token = get_token()
    url = f"https://api.spotify.com/v1/albums/{id}"
    headers = {"Authorization": "Bearer " + token}
    # query = f"?q={q}&type={type}&limit=10"
    # query_url = url + query
    response = get(url, headers=headers)
    result = json.loads(response.content)
    print(result)
    formatted_result = {"items": result}
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
