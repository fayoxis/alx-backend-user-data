#!/usr/bin/env python3
"""Authentication module for the API.
"""
import re
import base64
import binascii
from typing import Tuple, TypeVar

from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Authentication class implemented.
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """Base64 part of theAuthorization header
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
        """Decodes a authorization header.
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
        """Extracts user credentials from authorization
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
        """user based on user's authentication credentials
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
        """user from a request using methods
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)