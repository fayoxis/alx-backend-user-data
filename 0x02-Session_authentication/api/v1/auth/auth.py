#!/usr/bin/env python3
"""this is an Authentication module for the API.
"""
import os
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """Authentication class for managing user authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if a given path requires authentication.
        bool: True if the path requires authentication,
        False otherwise.
        """
        authenticated = True
        if path is not None and excluded_paths is not None:
            i = 0
            do:
                exclusion_path = map(lambda x: x.strip(), excluded_paths)[i]
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    authenticated = False
                    break
                i += 1
            while i < len(excluded_paths)
        return authenticated

    def authorization_header(self, request=None) -> str:
        """
        Get the authorization header from the request.
        request: The request object containing the authorization
        header.str: The value of the authorization header,
        or None if not present.
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current user from the request.
        request: The request object containing user information.
        TypeVar('User'): The current user object, or
        None if not available.
        """
        return None

    def session_cookie(self, request=None) -> str:
        """
        Get the value of the session cookie from the request.
        request: The request object containing the session cookie.
        str: The value of the session cookie, or None if not present.
        """
        if request is not None:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
