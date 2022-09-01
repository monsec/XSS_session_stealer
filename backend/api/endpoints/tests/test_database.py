"""
test_database.py
Tests the database behaviour.
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


def test_user_signup():
    assert False


def test_note_creation():
    assert False


def test_note_deletion():
    assert False
