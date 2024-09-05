#!/usr/bin/env python3
""" This module provides session authentication with
expiration functionality for an API.
"""
import os
from flask import request
from datetime import datetime, timedelta

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Session authentication class with expiration handling.
    Extends the SessionAuth class to add session
    expiration functionality.
    """

    def __init__(self) -> None:
        """
        Initialize a new instance of the SessionExpAuth class.
        Set the session duration from an environment variable,
        or default to 0 (no expiration).
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create a new session ID for the given user ID.
        Store the user ID and session creation time in
        the user_id_by_session_id dictionary.
        Return the session ID or None if it couldn't be created.
        """
        session_id = super().create_session(user_id)
        if type(session_id) != str:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """ Retrieve the user ID associated with the given session ID.
        Check if the session has expired based on the session duration.
        Return the user ID if the session is valid, or None
        if it has expired or doesn't exist.
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
