#!/usr/bin/env python3
"""
a Script for session authentication module for the API.
"""
from uuid import uuid4
from flask import request

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    a class for a session authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) ->str:
        """
        a method to create a session id
        """
        if type(user_id) is str: # checks if user id is a string
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        a method that gets a user id associated with given session id
        """
        if type(session_id) is str:
            return se;f.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """
        a method to retrieve a user with requested cookie
        """
        userId = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(userId)

    def destroy_session(self, request=None):
        """
        a methid to destroy session
        """
        session_id = self.session_cookie(request)
        userId = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or userId is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
