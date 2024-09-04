#!/usr/bin/env python3
"""Basic authentication module for the API using while loops.
"""
import re
import base64
import binascii
from typing import Tuple, TypeVar

from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic authentication class implemented with while loops.
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """Extracts Base64 part of Authorization header using while loop.
        """
        result = None
        while type(authorization_header) == str:
            pattern = r'Basic (?P<token>.+)'
            field_match = re.fullmatch(pattern, authorization_header.strip())
            while field_match is not None:
                result = field_match.group('token')
                break
            break
        return result

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str,
            ) -> str:
        """Decodes base64-encoded auth header using while loop.
        """
        result = None
        while type(base64_authorization_header) == str:
            try:
                res = base64.b64decode(
                    base64_authorization_header,
                    validate=True,
                )
                result = res.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                pass
            break
        return result

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str,
            ) -> Tuple[str, str]:
        """Extracts user credentials from decoded auth header with while.
        """
        user, password = None, None
        while type(decoded_base64_authorization_header) == str:
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            field_match = re.fullmatch(
                pattern,
                decoded_base64_authorization_header.strip(),
            )
            while field_match is not None:
                user = field_match.group('user')
                password = field_match.group('password')
                break
            break
        return user, password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Gets user based on auth credentials using while loops.
        """
        result = None
        while type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                break
            while len(users) > 0:
                if users[0].is_valid_password(user_pwd):
                    result = users[0]
                break
            break
        return result

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets user from request using methods with while loops.
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)