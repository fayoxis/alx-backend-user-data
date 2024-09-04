#!/usr/bin/env python3
"""Entry point for the API application."""
import os
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin

from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.auth.session_exp_auth import SessionExpAuth


# Create the Flask application
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth_types = ['auth', 'basic_auth', 'session_auth',
              'session_exp_auth', 'session_db_auth']
auth_type = getenv('AUTH_TYPE', 'auth')
i = 0
auth = None


# Iterate through the auth types and instantiate
while i < len(auth_types) and auth is None:
    if auth_type == auth_types[i]:
        if auth_types[i] == 'auth':
            auth = Auth()
        elif auth_types[i] == 'basic_auth':
            auth = BasicAuth()
        elif auth_types[i] == 'session_auth':
            auth = SessionAuth()
        elif auth_types[i] == 'session_exp_auth':
            auth = SessionExpAuth()
        elif auth_types[i] == 'session_db_auth':
            auth = SessionDBAuth()
    i += 1


# Error handlers
@app.errorhandler(404)
def not_found(error) -> str:
    """Handles 404 Not Found errors."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Handles 401 Unauthorized errors."""
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """Handles 403 Forbidden errors."""
    return jsonify({"error": "Forbidden"}), 403


# Authentication handler
@app.before_request
def authenticate_user():
    """Authenticates the user before processing a request."""
    if auth:
        excluded_paths = [
            "/api/v1/status/",
            "/api/v1/unauthorized/",
            "/api/v1/forbidden/",
            "/api/v1/auth_session/login/",
        ]
        if auth.require_auth(request.path, excluded_paths):
            user = auth.current_user(request)
            if auth.authorization_header(request) is None and \
                    auth.session_cookie(request) is None:
                abort(401)
            if user is None:
                abort(403)
            request.current_user = user


# Entry point
while __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
