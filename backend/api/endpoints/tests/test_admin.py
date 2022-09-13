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


def login(user_id: UUID):
    """Login Helper"""
    return AuthHandler().encode_token(user_id)


def test_signup(client: TestClient, test_db: Session):

    payload = {"username": "admin", "password": "password"}
    # request
    response = client.post("/admin/signup", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    # check database
    admin = (
        test_db.query(mdl.User)
        .filter(
            mdl.User.username == "admin",
        )
        .one_or_none()
    )
    assert admin.is_admin is True


def test_fetch_comments(client: TestClient, test_db: Session):
    # setup
    fac.User._meta.sqlalchemy_session = test_db
    fac.Comment._meta.sqlalchemy_session = test_db
    admin_id, comment_id = uuid4(), uuid4()
    fac.Comment.create(id=comment_id, comment="the website crashes!")
    fac.User.create(id=admin_id, username="admin", is_admin=True)

    # check that there is a comment in the db
    comment = (
        test_db.query(mdl.FeedbackComment)
        .filter(mdl.FeedbackComment.id == comment_id)
        .one_or_none()
    )

    assert comment is not None

    # request
    token = login(str(admin_id))
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/admin/feedback", headers=headers)
    res_data = response.json()
    print(res_data)
    assert response.status_code == status.HTTP_200_OK
    assert res_data is not None
    res_data[0]["comment"] == "the website crashes!"


def test_delete_comment(client: TestClient, test_db: Session):
    # setup
    fac.User._meta.sqlalchemy_session = test_db
    fac.Comment._meta.sqlalchemy_session = test_db
    admin_id, comment_id = uuid4(), uuid4()
    fac.Comment.create(id=comment_id, comment="the website crashes!")
    fac.User.create(id=admin_id, username="admin", is_admin=True)

    # request
    token = login(str(admin_id))
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/admin/feedback/{comment_id}", headers=headers)
    res_data = response.json()
    assert res_data is None
    assert response.status_code == status.HTTP_200_OK

    # check that the comment has been delete from the database
    comment = (
        test_db.query(mdl.FeedbackComment)
        .filter(mdl.FeedbackComment.id == comment_id)
        .one_or_none()
    )
    assert comment is None


def test_view_comment(client: TestClient, test_db: Session):
    # setup
    fac.User._meta.sqlalchemy_session = test_db
    fac.Comment._meta.sqlalchemy_session = test_db
    admin_id, comment_id = uuid4(), uuid4()
    fac.Comment.create(id=comment_id, comment="the website crashes!")
    fac.User.create(id=admin_id, username="admin", is_admin=True)

    # request
    token = login(str(admin_id))
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/admin/feedback/{comment_id}", headers=headers)
    res_data = response.json()
    assert res_data is not None
    assert response.status_code == status.HTTP_200_OK
    assert res_data["comment"] == "the website crashes!"
    assert res_data["id"] == str(comment_id)
