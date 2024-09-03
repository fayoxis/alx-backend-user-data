#!/usr/bin/env python3
"""This module handles authentication for the API.
"""
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """This class manages authentication-related operations
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a path requires authentication or not.
        path (str): The path to be checked for auth requirement.
        """
        if path is not None and excluded_paths is not None:
            i = 0
            while i < len(excluded_paths):
                exclusion_path = excluded_paths[i].strip()
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
                i += 1
        return True

    def authorization_header(self, request=None) -> str:
        """Retrieves the authorization header from the request.
        request (Optional[flask.Request]): The Flask request object.
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user associated with the request.
        request (Optional[flask.Request]): The Flask request object.
        """
        return None
