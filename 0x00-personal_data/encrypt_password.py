#!/usr/bin/env python3
"""
Created by Jenaide Sibolie
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    function that hash a password using salt
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    function that checks if hashed pwd was created
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
