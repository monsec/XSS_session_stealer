"""
test_user.py
Tests for the user endpoints
"""
from uuid import uuid4, UUID

# Package Imports
from fastapi.testclient import TestClient
from fastapi import status
from api.utils.auth import AuthHandler
from sqlalchemy.orm.session import Session

# Local Imports
import api.meta.database.model as mdl
import api.meta.database.factories as fac
from api.config import get_settings

settings = get_settings()


def test_signup(client: TestClient, test_db: Session):
    """
    This test ensures that the user can create a user.
    """

    # payload
    payload = {
        "username": "monsec",
        "password": "password",
    }

    # request
    response = client.post("/user/signup", json=payload)
    res_data = response.json()
    assert res_data is not None
    assert response.status_code == status.HTTP_201_CREATED

    # check that the user was createds
    assert (
        test_db.query(mdl.User).filter(mdl.User.username == "monsec").one_or_none()
        is not None
    )
    assert False


def test_signup_lowercase_it(client: TestClient, test_db: Session):
    """
    This test ensures that when signing up, the user gets
    lowercased to avoid collision
    """
    assert False


def test_signup_same_username(client: TestClient, test_db: Session):
    """
    This test ensures that only a unique username exists.
    """
    assert False


def test_login(client: TestClient, test_db: Session):
    "Test that the login works"
    assert False


def test_login(client: TestClient, test_db: Session):
    """
    This test ensures that the user logs in with the lowercase
    attempt two 'MONSEC' and 'monsec' are the same.
    """
    assert False


def test_post_comment_feedback(client: TestClient, test_db: Session):
    "Test that the user can post"
    assert False
