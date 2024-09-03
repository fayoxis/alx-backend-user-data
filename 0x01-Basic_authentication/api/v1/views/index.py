#!/usr/bin/env python3
"""Module containing Index views for the API.
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """Handles GET requests to /api/v1/status.
    
    Returns:
      A JSON response indicating the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """Handles GET requests to /api/v1/stats.
    
    Returns:
      A JSON response with the count of each object type.
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized/', strict_slashes=False)
def unauthorized() -> None:
    """Handles GET requests to /api/v1/unauthorized.
    
    Triggers a 401 Unauthorized error response.
    """
    abort(401)


@app_views.route('/forbidden/', strict_slashes=False)
def forbidden() -> None:
    """Handles GET requests to /api/v1/forbidden.
    
    Triggers a 403 Forbidden error response.
    """
    abort(403)
