"""
user.py
The users will be able to send feedback to the admin from here.
"""
from fastapi import APIRouter
from fastapi import status

# Local imports
from api.config import get_settings
from api.utils.auth import AuthHandler

# -------------------
# Setup Router
# -------------------

router = APIRouter()
settings = get_settings()
auth_handler = AuthHandler()

# Endpoints

# TODO:


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_account():
    pass
