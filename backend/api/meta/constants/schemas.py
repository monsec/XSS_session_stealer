"""
Schemas.py
Schemas used for validation of request fields.
"""
# Package imports
from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4, UUID

from sqlalchemy import TIMESTAMP

# Local imports
from api.config import get_settings

# ----------------------
settings = get_settings()
# ----------------------


# ---------------
# User Schemas
# ---------------


class AuthDetails(BaseModel):
    username: str = Field(
        title="Account username",
        example="monsec",
    )
    password: str = Field(
        title="The password for the username",
        example="Password123",
    )


# --------------
# Comment Schema
# --------------


class CommentFeedback(BaseModel):
    comment: str = Field(
        title="The comment from the user",
        example="The website crashes.",
    )


class CommentObject(BaseModel):
    id: UUID = Field(
        title="The UUID of the note",
        example=uuid4(),
    )
    comment: str = Field(
        title="The comment from the user",
        example="The website crashes.",
    )
    created_date: str = Field(
        title="The date the comment was created",
    )
