#!/usr/bin/env python3
"""Session authentication with expiration
and storage support for the API."""
from flask import request
from datetime import datetime, timedelta

from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session authentication class with expiration and
    storage support. Manages user sessions, including
    creation, retrieval, and destruction.
    """

    def create_session(self, user_id=None) -> str:
        """Creates and stores a session id for the user.
        """
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve the user ID associated with a given session ID.
        Returns the user ID or None if the session is
        invalid or expired.
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        while len(sessions) > 0:
            cur_time = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            exp_time = sessions[0].created_at + time_span
            if exp_time >= cur_time:
                return sessions[0].user_id
        return None

    def destroy_session(self, request=None) -> bool:
        """Invalidate and remove an authenticated session.
        Returns True if the session was successfully
        destroyed, False otherwise.
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        while len(sessions) > 0:
            sessions[0].remove()
            return True
        return False
