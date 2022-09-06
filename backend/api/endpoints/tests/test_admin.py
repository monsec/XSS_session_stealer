"""
test_admin.py
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

    payload = {"username": "admin", "password": "password"}
    # request
    response = client.post("/admin/signup", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    # check database
    admin = test_db.query(mdl.User).filter(mdl.User.username == "admin").one_or_none()
    assert admin.is_admin is True


def test_fetch_comments(client: TestClient, test_db: Session):
    assert False


def test_delete_comment(client: TestClient, test_db: Session):
    assert False


def test_view_comment(client: TestClient, test_db: Session):
    assert False
