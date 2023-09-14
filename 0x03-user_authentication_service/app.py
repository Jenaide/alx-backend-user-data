#!/usr/bin/env python3
"""
A standard flask app with user authentication
"""
from flask import Flask, jsonify, request, abort, redirect

from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home() -> str:
    """
    flask route with a GET method
    Return:
        homepage
    """
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """
    flask user route with a POST method
    Returns:
        the created user
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    flask session route with a POST method
    Return:
        the user login
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response_data = {"email": email, "message": "logged in"}
        response = make_response(jsonify(response_data), 200)
        return response
    else:
        abort(401)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
