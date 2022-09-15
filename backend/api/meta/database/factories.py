"""
factories.py
Factories for easily creating test data in our tables
"""

# System Imports
import random

# import string
from uuid import uuid4, UUID
from sqlalchemy.orm import Session

import api.meta.database.model as mdl

# Package Imports
from factory import (
    alchemy,
    Faker,
    LazyAttribute,
    SubFactory,
    RelatedFactory,
    List as FakerList,
)


class User(alchemy.SQLAlchemyModelFactory):
    username = Faker("lexify", text="username-????")
    password = Faker("lexify", text="password-????")

    class Meta:
        model = mdl.User


class Comment(alchemy.SQLAlchemyModelFactory):
    comment = Faker("lexify", text="??????? ???????? ????????")

    class Meta:
        model = mdl.FeedbackComment
