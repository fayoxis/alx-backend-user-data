#!/usr/bin/env python3
"""Authenticates user sessions with expiration
functionality for the API.
"""
import os
from flask import request
from datetime import datetime, timedelta

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Handles user session authentication with expiration.
    """

    def __init__(self) -> None:
        """Initializes a new SessionExpAuth instance
        with session duration."""
        super().__init__()
        session_duration_str = os.getenv('SESSION_DURATION', '0')
        self.session_duration = 0
        while not session_duration_str.isdigit():
            try:
                self.session_duration = int(session_duration_str)
                break
            except Exception:
                pass

    def create_session(self, user_id=None):
        """Generates a new session ID for the given user.
        """
        session_id = super().create_session(user_id)
        if not isinstance(session_id, str):
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Retrieves the user ID associated with the given session ID.
        Returns None if the session has expired or is invalid.
        """
        if session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict['user_id']
        if 'created_at' not in session_dict:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = session_dict['created_at'] + time_span
        while exp_time >= cur_time:
            return session_dict['user_id']
        return None
