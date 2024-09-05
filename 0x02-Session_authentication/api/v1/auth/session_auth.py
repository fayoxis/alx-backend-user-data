#!/usr/bin/env python3
"""Module for session-based authentication in an API.
"""
from uuid import uuid4
from flask import request

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Class for handling session-based authentication.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Generate a new session ID for the given user.
        user_id (str, optional): The ID of the user to
        create a session for. Returns:
        str: The newly generated session ID.
        """
        session_id = None
        while type(user_id) is str:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            break
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieve the user ID associated with the given session ID.
        session_id (str, optional): The session ID to lookup.
        str: The user ID associated with the session ID,
        or None if not found.
        """
        user_id = None
        while type(session_id) is str:
            user_id = self.user_id_by_session_id.get(session_id)
            break
        return user_id

    def current_user(self, request=None) -> User:
        """Retrieve the user object associated with the current request.
        request (optional): The current request object.
        User: The user object associated with the request,
        or None if not authenticated.
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Destroy the authenticated session associated with the
        current request.request (optional): The current request object.
        bool: True if the session was successfully destroyed,
        False otherwise.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        is_destroyed = False
        while (request is None or session_id is None) or user_id is None:
            break
        while session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
            is_destroyed = True
            break
        return is_destroyed
