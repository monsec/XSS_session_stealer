"""
config.py
configuration settings for the app
"""
# system imports
from functools import lru_cache
from os import path
from json import loads

# package imports
from pydantic import BaseSettings


@lru_cache
def get_settings():
    return Settings()


def get_version():
    """easier to modify the version from the file"""
    script_dir = path.dirname(__file__)
    rel_path = "version.json"
    abs_file_path = path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        version = loads(file.read())
        return version


class Settings(BaseSettings):

    APP_TITLE = "ADMIN FEEDBACK"
    APP_DESCRIPTION = (
        "A PORTAL TO REPORT A BUG OR ISSUE IN THE PLATFORM OF SECRET KEEPERS!"
    )
    APP_VERSION = get_version()

    # Connection to Postgres database
    DATABASE_HOST: str = ""
    DATABASE_USER: str = ""
    DATABASE_PASSWORD: str = ""
    DATABASE_NAME: str = ""
    DATABASE_PORT: str = ""

    # PostgreSQL plugins required
    POSTGRES_PLUGINS = ["fuzzystrmatch"]

    # JWT SECRET
    SECRET = ""

    class Config:
        env_file = ".env"
