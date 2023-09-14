#!/usr/bin/env python3
"""
Auth file
"""
import bcrypt
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from user import User
from db import DB


def _hash_password(password: str) -> bytes:
    """
    a hashed password method
    """
    #generates a random salt
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_pwd

def _generate_uuid() -> str:
    """
    a method that generates a uuid
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        a method that registers a user into the database
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        a method that checks if its a valid user thats login in
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """
        a method that creates a new session for the user
        """
        try:
            user = self._db.find_user_by(email=email)

            if user is None:
                return None
            else:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        a method to get a user based on a spesific session
        """
        user = None
        try:
            if session_id is None:
                return None
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None


    def destroy_session(self, user_id: int) -> None:
        """
        a method to destroy a session
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

