#!/usr/bin/env python3
"""Basic authentication module for the API.
"""
import re
import base64
from typing import Tuple, TypeVar
import binascii

from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    Standard Authentication class
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        base64 extraction part of the authorization header for the basic auth class.
        """
        if type(authorization_header) == str:
            pattern = r'Basic (?P<token>.+)'
            field = re.fullmatch(pattern, authorization_header.strip())
            if field is not None:
                return field.group('token')
        return None

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        method to decode a base64-encoded auth header
        """
        if type(base64_authorization_header) == str:
            try:
                results = base64.b64decode(
                        base64_authorization_header,
                        validate = True,
                )
                return results.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        method that extracts user credentials form base64 auth header
        """
        if type(decoded_base64_authorization_header) == str:
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            field = re.fullmatch(pattern, decoded_base64_authorization_header.strip())
            if field is not None:
                user = field.group('user')
                password = field.group('password')
                return user, password
            return None, None

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        method that retreives a user based on the user's auth credentials
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if user[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        methods that retrieves the user upon request
        """
        auth_header = self.authorization_header(request)
        b64_header_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
