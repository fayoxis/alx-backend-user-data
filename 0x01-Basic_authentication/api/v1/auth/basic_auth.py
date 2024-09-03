#!/usr/bin/env python3
"""Module for handling Basic Authentication for the API."""
import re
import base64
import binascii
from typing import Tuple, TypeVar

from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Class for Basic Authentication."""
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """Extract Base64 part of Authorization header for Basic Auth."""
        base64_token = None
        pattern = r'Basic (?P<token>.+)'
        while type(authorization_header) == str:
            field_match = re.fullmatch(pattern, authorization_header.strip())
            if field_match is not None:
                base64_token = field_match.group('token')
                break
        return base64_token

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str,
            ) -> str:
        """Decode a base64-encoded authorization header."""
        decoded_header = None
        while type(base64_authorization_header) == str:
            try:
                res = base64.b64decode(
                    base64_authorization_header,
                    validate=True,
                )
                decoded_header = res.decode('utf-8')
                break
            except (binascii.Error, UnicodeDecodeError):
                break
        return decoded_header

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str,
            ) -> Tuple[str, str]:
        """Extract user credentials from decoded Basic Auth header."""
        user, password = None, None
        pattern = r'(?P<user>[^:]+):(?P<password>.+)'
        while type(decoded_base64_authorization_header) == str:
            field_match = re.fullmatch(
                pattern,
                decoded_base64_authorization_header.strip(),
            )
            if field_match is not None:
                user = field_match.group('user')
                password = field_match.group('password')
                break
        return user, password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Retrieve user based on authentication credentials."""
        user_obj = None
        while type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                break
            if len(users) <= 0:
                break
            if users[0].is_valid_password(user_pwd):
                user_obj = users[0]
                break
        return user_obj

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve user from a request."""
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
