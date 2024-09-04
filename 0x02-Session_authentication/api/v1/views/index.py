#!/usr/bin/env python3
"""This module defines the routes for the Index views."""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """Retrieves the status of the API.
    Returns:
        A JSON response containing the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """Retrieves the statistics of the application.
    Returns:
        A JSON response containing the count of users.
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized/', strict_slashes=False)
def unauthorized() -> None:
    """Raises an Unauthorized error.
    Returns:
        An Unauthorized error (HTTP status code 401).
    """
    abort(401)


@app_views.route('/forbidden/', strict_slashes=False)
def forbidden() -> None:
    """Raises a Forbidden error.
    Returns:
        A Forbidden error (HTTP status code 403).
    """
    abort(403)
