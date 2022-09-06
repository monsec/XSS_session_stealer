"""
admin.py
The admin panel, administrator will be able to see the feedback sent by users here.
"""
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

# Local imports
from api.config import get_settings
from api.utils.auth import AuthHandler
from api.utils.auth import require_user_account
from api.meta.constants.schemas import AuthDetails
from api.utils.database import get_db
from api.meta.constants.errors import (
    USERNAME_TAKEN,
    SOMETHING_WENT_WRONG,
)
from api.meta.database.model import User

# -------------------
# Setup Router
# -------------------

router = APIRouter()
settings = get_settings()
auth_handler = AuthHandler()


requires_db = Depends(get_db)
requires_user_account = Depends(require_user_account)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_account(auth_handler: AuthDetails, db: Session = requires_db):
    """
    Create admin account
    Args:
        - username: str
        - password: str

    Returns: None
    """

    security = AuthHandler()
    # check that the username is not in the db
    user_exists = (
        db.query(User)
        .filter(
            User.username.ilike(auth_handler.username),
        )
        .one_or_none()
    )

    # if the user exists, raise error
    if user_exists is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=USERNAME_TAKEN,
        )

    # else: add it to the db

    # hash password
    password = security.get_password_hash(auth_handler.password)
    username = auth_handler.username.lower()
    new_admin = User(
        username=username,
        password=password,
        is_admin=True,
    )

    # add user to db
    try:
        db.add(new_admin)
        db.commit()

    # if any error when adding, raise it
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=SOMETHING_WENT_WRONG,
        )


@router.post("/login", status_code=status.HTTP_200_OK)
def login(auth_handler: AuthDetails, db: Session = requires_user_account):
    pass


@router.get("/feedback", status_code=status.HTTP_200_OK)
def post_feedback_comment():
    pass
