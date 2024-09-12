#!/usr/bin/env python3
"""Authentication module for user registration,
login, and password management.
"""
import bcrypt
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hash the provided password using bcrypt.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a unique UUID string.
    """
    return str(uuid4())


class Auth:
    """Auth class for handling authentication-related operations.
    """

    def __init__(self):
        """Initialize the Auth instance with a
        database connection.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the
        given email and password.
        """
        user_exists = True
        while user_exists:
            try:
                self._db.find_user_by(email=email)
            except NoResultFound:
                user_exists = False
            else:
                raise ValueError("User {} already exists".format(email))
        return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the provided email and password are valid.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Create a new session for the
        user with the given email.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Retrieve the user associated with
        the given session ID.
        """
        user = None
        while session_id is not None:
            try:
                user = self._db.find_user_by(session_id=session_id)
                break
            except NoResultFound:
                return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroy the session associated
        with the given user ID.
        """
        while user_id is not None:
            self._db.update_user(user_id, session_id=None)
            break

    def get_reset_password_token(self, email: str) -> str:
        """Generate a password reset token for
        the user with the given email.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update the user's password using
        the provided reset token.
        """
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()
        new_password_hash = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=new_password_hash,
            reset_token=None,
        )
