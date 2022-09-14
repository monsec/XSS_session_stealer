"""
admin.py
The admin panel, administrator will be able
to see the feedback sent by users here.
"""
from typing import Dict, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

# Local imports
from api.config import get_settings
from api.utils.auth import AuthHandler
from api.utils.auth import require_user_account
from api.meta.constants.schemas import AuthDetails, CommentObject
from api.utils.database import get_db
from api.meta.constants.errors import (
    USERNAME_TAKEN,
    SOMETHING_WENT_WRONG,
    NOT_AUTHORIZED,
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


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
def create_account(
    auth_details: AuthDetails,
    db: Session = requires_db,
) -> None:
    """
    Create admin account
    Args:
        - username: str
        - password: str

    Return:
        - None
    """

    security = AuthHandler()
    # check that the username is not in the db
    user_exists = (
        db.query(User)
        .filter(
            User.username.ilike(auth_details.username),
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
    password = security.get_password_hash(auth_details.password)
    username = auth_details.username.lower()
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


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, str],
)
def login(
    auth_details: AuthDetails,
    db: Session = requires_db,
)->Dict[str,str]:
    """
    Login for admin accounts
    Args:
        - username: str
        - password: str
    Return:
        - token: dict
    """

    security = AuthHandler()
    username = auth_details.username.lower()
    password = auth_details.password
    hashed_password = security.get_password_hash(password)
    matches = security.verify_password(
        password,
        hashed_password,
    )
    # check that the credentials match a user
    user = db.query(User).filter(User.username == username).one_or_none()
    if (user is None) or (user.is_admin is False) or not (matches):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # else return admin token
    token = security.encode_token(str(user.id))
    return {"token": token}


@router.get(
    "/feedback",
    status_code=status.HTTP_200_OK,
    response_model=List[CommentObject]
)
def post_feedback_comment(
    user: User = requires_user_account,
    db: Session = requires_db,
) -> List[CommentObject]:
    """
    Return all the feedback comments
    Args:
        - None
    Return:
        - comments: List[CommentObject]
    """

    # check if the user requesting is an admin
    if user.is_admin is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=NOT_AUTHORIZED,
        )

    comments = db.query(FeedbackComment).all()

    return [
        CommentObject(
            id=comment.id,
            comment=comment.comment,
        )
        for comment in comments
    ]


@router.get(
    "/feedback/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=CommentObject,
)
def view_feedback_comment(
    comment_id: UUID,
    user: User = requires_user_account,
    db: Session = requires_db,
) -> CommentObject:
    """
    Return a single feedback comment
    Args:
        - comment_id in query
    Returns:
        - CommentObject
    """

    # check that is admin
    if user.is_admin is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    # get the comment from the db
    comment = (
        db.query(FeedbackComment)
        .filter(
            FeedbackComment.id == comment_id,
        )
        .one_or_none()
    )

    # if None raise 404
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return CommentObject(
        id=comment.id,
        comment=comment.comment,
    )


@router.delete(
    "/feedback/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=None
)
def delete_feedback_comment(
    comment_id: UUID,
    user: User = requires_user_account,
    db: Session = requires_db,
)-> None:
    """
    Delete note from db
    Args:
        - comment_id in query
    Returns:
        - None
    """

    # check that is admin
    if user.is_admin is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    # fetch the comment from the db
    comment = (
        db.query(FeedbackComment)
        .filter(
            FeedbackComment.id == comment_id,
        )
        .one_or_none()
    )
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # delete if no errors
    db.delete(comment)
    db.commit()
