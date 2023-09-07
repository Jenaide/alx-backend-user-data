#!/usr/bin/env python3
"""
Script for the session authenticating views.
"""
import os
from typing import Tuple
from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views



@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """
    POST method /api/v1/auth_session/login
    Return:
        JSON representation of a user object
    """
    err_results = {"error": "User not found for this email string"}
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email not found"}), 400
    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password not found"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(err_results), 404
    if len(users) <= 0:
        return jsonify(err_results), 404
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(users[0], 'id'))
        result = jsonify(users[0].to_json())
        result.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return result
    return jsonify({"error": "incorrect password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """
    DELETE method api/v1/auth_session/logout
    Return:
        empty jsonify object
    """
    from api.v1.app import auth
    destroyed = auth.destroy_session(request)
    if not destroyed:
        abort(404)
    return jsonify({})
