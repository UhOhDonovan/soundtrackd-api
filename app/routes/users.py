from typing import Union
from fastapi import HTTPException, Response, APIRouter
from pydantic import BaseModel
import getpass
import re
import hashlib

router = APIRouter()
