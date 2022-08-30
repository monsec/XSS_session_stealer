"""
admin.py
The admin panel, administrator will be able to see the feedback sent by users here.
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


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_admin_account():
    pass
