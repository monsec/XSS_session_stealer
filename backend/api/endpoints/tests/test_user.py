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
from api.meta.constants.errors import USERNAME_TAKEN
import api.meta.database.model as mdl
import api.meta.database.factories as fac
from api.config import get_settings

settings = get_settings()


def login(user_id: UUID):
    """Login Helper"""
    return AuthHandler().encode_token(user_id)


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
    assert res_data is None  # no response, just status
    assert response.status_code == status.HTTP_201_CREATED

    # check that the user was created
    assert (
        test_db.query(mdl.User).filter(mdl.User.username == "monsec").one_or_none()
        is not None
    )


def test_signup_lowercase_it(client: TestClient, test_db: Session):
    """
    This test ensures that when signing up, the user gets
    lowercased to avoid collision
    """
    # payload
    payload = {
        "username": "MONSEC",
        "password": "password",
    }

    # request
    response = client.post("/user/signup", json=payload)
    res_data = response.json()
    assert res_data is None  # no response, just status
    assert response.status_code == status.HTTP_201_CREATED

    # check that the user was created in lowercase
    query = (
        test_db.query(mdl.User).filter(mdl.User.username.ilike("MONSEC")).one_or_none()
    )

    assert query.username == "monsec"


def test_signup_same_username(client: TestClient, test_db: Session):
    """
    This test ensures that only a unique username exists.
    """

    fac.User._meta.sqlalchemy_session = test_db
    fac.User.create(id=uuid4(), username="monsec")

    # request
    payload = {"username": "MONSEC", "password": "test"}
    response = client.post("/user/signup", json=payload)
    res_data = response.json()
    assert res_data is not None  # error response
    assert res_data["detail"]["msg"] == USERNAME_TAKEN

    # check that there is only 1 in the db
    assert test_db.query(mdl.User).filter(mdl.User.username == "monsec").count() == 1


def test_login(client: TestClient, test_db: Session):
    """
    Test that the login works
    """
    fac.User._meta.sqlalchemy_session = test_db
    security = AuthHandler()

    # create user
    user_id = uuid4()
    password = security.get_password_hash("password")
    fac.User.create(id=user_id, username="monsec", password=password)

    print(test_db.query(mdl.User).filter(mdl.User.id == user_id).first())

    # request
    payload = {"username": "monsec", "password": "password"}
    response = client.post("/user/login", json=payload)
    res_data = response.json()
    assert response is not None
    print(res_data)
    token = security.decode_token(res_data["token"])
    assert token["id"] == str(user_id)


def test_login_lowercase(client: TestClient, test_db: Session):
    """
    This test ensures that the user logs in with the lowercase
    attempt two 'MONSEC' and 'monsec' are the same.
    """
    fac.User._meta.sqlalchemy_session = test_db
    security = AuthHandler()
    password = security.get_password_hash("password")
    # create user
    user_id = uuid4()
    fac.User.create(id=user_id, username="monsec", password=password)

    # request
    payload = {"username": "MONSEC", "password": "password"}
    response = client.post("/user/login", json=payload)
    res_data = response.json()
    assert response is not None
    token = security.decode_token(res_data["token"])
    assert token["id"] == str(user_id)


def test_post_comment_feedback(client: TestClient, test_db: Session):
    "Test that the user can post feedback"
    fac.User._meta.sqlalchemy_session = test_db
    user_id = str(uuid4())
    fac.User.create(id=user_id, username="monsec", password="password")

    # request
    token = login(user_id)
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"comment": "the website crashes!"}
    response = client.post("/user/feedback", json=payload, headers=headers)
    res_data = response.json()
    assert res_data is None
    assert response.status_code == status.HTTP_201_CREATED

    # check that it has been posted on the db
    query = test_db.query(mdl.FeedbackComment).first()
    assert query is not None
    assert query.comment == "the website crashes!"
