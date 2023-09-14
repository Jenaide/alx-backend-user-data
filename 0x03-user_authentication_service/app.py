#!/usr/bin/env python3
"""
A standard flask app with user authentication
"""
from flask import Flask, jsonify, request, abort, redirect, make_response

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
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """
    flask session route with a delete method
    Return:
        after logout it redirects to home page
    """
    try:
        session_id = request.cookies.get("session_id")
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("/")
        else:
            abort(403)
    except ValueError:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
    flask profile route
    Returns:
        the user's profile info
    """
    try:
        session_id = request.cookies.get("session_id")
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            response_data = {"email": user.email}
            return jsonify(response_data), 200
        else:
            abort(403)
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    flask route to get the password that user reset
    Returns:
        the user password
    """
    try:
        email = request.form.get("email")
        user = AUTH.get_user_by_email(email)

        if user:
            resetToken = AUTH.get_reset_password_token(email)
            response_data = {
                    "email": email,
                    "reset_token": resetToken
            }
            return jsonify(response_data), 200
        else:
            abort(403)
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    flask route to update user password

    Return:
        the user's updated password
    """
    try:
        email = request.form.get("email")
        resetToken = request.form.get("reset_token")
        new_pwd = request.form.get("new_password")

        AUTH.update_password(resetToken, new_pwd)

        response_data = {
                "email": email,
                "message": "Password updated"
        }
        return jsonify(response_data), 200
    except ValueError:
        abort(403)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
