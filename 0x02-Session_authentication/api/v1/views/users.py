#!/usr/bin/env python3
"""This module contains the User views for a RESTful API."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """Retrieve a list of all User objects in JSON format."""
    all_users = []
    users = User.all()
    index = 0
    while index < len(users):
        all_users.append(users[index].to_json())
        index += 1
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """Retrieve a specific User object in JSON format.
    If the user_id is 'me', return the current user.
    If the user_id is not found, return a 404 error.
    """
    keep_going = True
    while keep_going:
        if user_id is None:
            abort(404)
            keep_going = False
        elif user_id == 'me':
            if request.current_user is None:
                abort(404)
                keep_going = False
            else:
                return jsonify(request.current_user.to_json())
                keep_going = False
        else:
            user = User.get(user_id)
            if user is None:
                abort(404)
                keep_going = False
            else:
                return jsonify(user.to_json())
                keep_going = False


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """Delete a specific User object.
    If the user_id is not found, return a 404 error.
    If the user is deleted successfully, return an empty JSON.
    """
    keep_going = True
    while keep_going:
        if user_id is None:
            abort(404)
            keep_going = False
        else:
            user = User.get(user_id)
            if user is None:
                abort(404)
                keep_going = False
            else:
                user.remove()
                return jsonify({}), 200
                keep_going = False


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """Create a new User object.
    The request body should contain the 'email' and 'password' fields.
    The 'first_name' and 'last_name' fields are optional.
    If the request is valid, return the new User object in JSON format
    with status code 201. If invalid, return a 400 error.
    """
    rj = None
    error_msg = None
    try:
        rj = request.get_json()
    except Exception as e:
        error_msg = "Wrong format"
    while error_msg is None:
        if rj is None:
            error_msg = "Wrong format"
            break
        elif rj.get("email", "") == "":
            error_msg = "email missing"
            break
        elif rj.get("password", "") == "":
            error_msg = "password missing"
            break
        else:
            try:
                user = User()
                user.email = rj.get("email")
                user.password = rj.get("password")
                user.first_name = rj.get("first_name")
                user.last_name = rj.get("last_name")
                user.save()
                return jsonify(user.to_json()), 201
            except Exception as e:
                error_msg = "Can't create User: {}".format(e)
                break
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """Update a specific User object.
    The request body should contain the 'first_name' and/or 'last_name'
    fields to be updated.
    If the user_id is not found, return a 404 error.
    If the request is invalid, return a 400 error.
    If successful, return the updated User object in JSON.
    """
    keep_going = True
    while keep_going:
        if user_id is None:
            abort(404)
            keep_going = False
        else:
            user = User.get(user_id)
            if user is None:
                abort(404)
                keep_going = False
            else:
                rj = None
                try:
                    rj = request.get_json()
                except Exception as e:
                    rj = None
                if rj is None:
                    return jsonify({'error': "Wrong format"}), 400
                    keep_going = False
                else:
                    if rj.get('first_name') is not None:
                        user.first_name = rj.get('first_name')
                    if rj.get('last_name') is not None:
                        user.last_name = rj.get('last_name')
                    user.save()
                    return jsonify(user.to_json()), 200
                    keep_going = False
