"""
user.py
The users will be able to send feedback to the admin from here.
"""
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

# Local imports
from api.config import get_settings
from api.utils.auth import AuthHandler
from api.meta.constants.schemas import AuthDetails, CommentFeedback
from api.utils.database import get_db
from api.utils.auth import require_user_account
from api.meta.constants.errors import (
    USERNAME_TAKEN,
    SOMETHING_WENT_WRONG,
    INVALID_TOKEN,
    INVALID_LOGIN,
)
from api.meta.database.model import User, FeedbackComment

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
    This function creates a user that is not registered yet.
    Args:
        - username: str
        - password: str

    Returns: None
    """

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
    password = AuthHandler.get_password_hash(auth_handler.password)
    username = auth_handler.username.lower()
    new_user = User(
        username=username,
        password=password,
    )

    # add user to db
    try:
        db.add(new_user)
        db.commit()

    # if any error when adding, raise it
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=SOMETHING_WENT_WRONG,
        )


@router.post("/login", status_code=status.HTTP_200_OK)
def login(auth_handler: AuthDetails, db: Session = requires_db):
    """
    This function checks the username,password passed and returns
    a token if successful
    Args:
        - username:str
        - password:str
    Returns:
        token:str (JWT)
    """

    # check  that the user username and password matches the db
    security = AuthHandler()
    username = auth_handler.username.lower()
    hashed_password = security.get_password_hash(auth_handler.password)

    user = (
        db.query(User)
        .filter(
            and_(
                User.username == username,
                User.password == hashed_password,
            )
        )
        .one_or_none()
    )

    # check if the user matches
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_LOGIN,
        )

    # else: return token
    token = AuthHandler.encode_token(user.id)
    return {"token": token}


@router.post("/feedback", status_code=status.HTTP_200_OK)
def fetch_feedback_comments(
    comment: CommentFeedback,
    user: User = requires_user_account,
    db: Session = requires_db,
):

    pass
