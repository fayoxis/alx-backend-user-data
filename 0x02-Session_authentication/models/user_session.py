#!/usr/bin/env python3
"""
This module defines the UserSession class,
which represents a user session.
"""
from models.base import Base


class UserSession(Base):
    """ UserSession class.
    This class inherits from the Base class and is
    used to store and manage user session data. Each
    instance of this class represents a single user
    session and contains the user's ID and the session ID.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a new UserSession instance.
        *args: Positional arguments.
        **kwargs: Keyword arguments, including:
        user_id (str): The ID of the user associated
        with the session. session_id (str): The unique
        identifier for the session.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
