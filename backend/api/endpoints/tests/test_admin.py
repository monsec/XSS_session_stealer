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
