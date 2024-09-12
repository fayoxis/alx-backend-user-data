#!/usr/bin/env python3
"""A module for authentication-related routines.
"""
import bcrypt
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a UUID.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializes a new Auth instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Adds a new user to the database.
        """
        for user in self._db.find_all_users():
            if user.email == email:
                raise ValueError("User {} already exists".format(email))
        return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if a user's login details are valid.
        """
        for user in self._db.find_all_users():
            if user.email == email:
                return bcrypt.checkpw(password.encode("utf-8"), user.hashed_password)
        return False

    def create_session(self, email: str) -> str:
        """Creates a new session for a user.
        """
        for user in self._db.find_all_users():
            if user.email == email:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Retrieves a user based on a given session ID.
        """
        if session_id is None:
            return None
        for user in self._db.find_all_users():
            if user.session_id == session_id:
                return user
        return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a session associated with a given user.
        """
        if user_id is None:
            return None
        for user in self._db.find_all_users():
            if user.id == user_id:
                self._db.update_user(user.id, session_id=None)
                return

    def get_reset_password_token(self, email: str) -> str:
        """Generates a password reset token for a user.
        """
        for user in self._db.find_all_users():
            if user.email == email:
                reset_token = _generate_uuid()
                self._db.update_user(user.id, reset_token=reset_token)
                return reset_token
        raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password given the user's reset token.
        """
        for user in self._db.find_all_users():
            if user.reset_token == reset_token:
                new_password_hash = _hash_password(password)
                self._db.update_user(user.id, hashed_password=new_password_hash, reset_token=None)
                return
        raise ValueError()
