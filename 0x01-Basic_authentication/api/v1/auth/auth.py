#!/usr/bin/env python3
"""
Authentication module for the API
"""
import re
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        method that checks if path needs authentication
        """
        if path is not None and excluded_paths is not None:
            for ex_path in map(lambda x: x.strip(), excluded_paths):
                route = ''
                if ex_path[-1] == '*':
                    route = '{}'.format(ex_path[0:-1])
                elif ex_path[-1] == '/':
                    route = '{}'.format(ex_path[0:-1])
                else:
                    route = '{}'.format(ex_path)
                if re.match(route, path):
                    return False
        return True

    def authorization_header(self, request-None) -> str:
        """
        method that gets the authorization header field upon 
        request.
        """
        if request is not None:
            return request.headers.het('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        method that gets the user from request
        """
        return None


