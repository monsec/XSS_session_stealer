"""
model.py
Defines our database model for use in SQLAlchemy
"""
# Package imports
import time
from datetime import datetime
from sqlalchemy import (
    MetaData,
    String,
    Column,
    Boolean,
    text,
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy_utils import generic_repr
import pytz


meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

newUUIDSql = (
    "overlay(overlay(md5(random()::text || ':' || clock_timestamp()::text) "
    "placing '4' from 13) placing '8' from 17)::uuid"
)


def time_now():
    """Return current time in AEST"""
    return datetime.now(pytz.timezone("Australia/Melbourne"))


def get_now(self):
    """
    If we don't use a function here,
    SQLAlchemy doesn't properly get the time each update
    """
    return int(time.time())


Base = declarative_base(metadata=meta)


#############
# USER TABLES
#############


@generic_repr
class User(Base):
    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        server_default=text(newUUIDSql),
    )

    created_date = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=time_now,
    )
    updated_date = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=time_now,
        onupdate=time_now,
    )

    username = Column(
        String(64),
        nullable=False,
    )
    password = Column(
        String(128),
        nullable=False,
    )
    is_admin = Column(
        Boolean,
        nullable=False,
        default=False,
    )


@generic_repr
class FeedbackComment(Base):
    __tablename__ = "feeback_comment"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text(newUUIDSql),
        unique=True,
    )

    created_date = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=time_now,
    )

    updated_date = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=time_now,
        onupdate=time_now,
    )

    comment = Column(
        String(512),
        nullable=False,
    )
