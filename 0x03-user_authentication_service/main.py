#!/usr/bin/env python3
"""End-to-end integration test suite for the user
management API. This script tests various
functionalities including user registration,
authentication, profile management, and password reset.
"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Attempts to register a new user and
    verifies the response. Also checks for proper
    handling of duplicate registration attempts.
    """
    url = "{}/users".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}
    res = requests.post(url, data=body)
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempts to log in with an incorrect
    password and verifies that the server
    responds with the appropriate error.
    """
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """Attempts to log in with correct credentials
    and verifies that the server responds with
    a successful login message. Returns the
    session ID for further authenticated requests.
    """
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """Attempts to access the user profile without being
    logged in and verifies that the server denies access.
    """
    url = "{}/profile".format(BASE_URL)
    res = requests.get(url)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """Attempts to access the user profile while
    logged in and verifies that the server provides
    the profile information..
    """
    url = "{}/profile".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.get(url, cookies=req_cookies)
    assert res.status_code == 200
    assert "email" in res.json()


def log_out(session_id: str) -> None:
    """Attempts to log out of an active session and
    verifies that the server responds with a
    logout confirmation
    """
    url = "{}/sessions".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.delete(url, cookies=req_cookies)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Requests a password reset token for a
    given email and verifies that the server
    provides a valid reset token..
    """
    url = "{}/reset_password".format(BASE_URL)
    body = {'email': email}
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert "email" in res.json()
    assert res.json()["email"] == email
    assert "reset_token" in res.json()
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Attempts to update the user's password
    using a reset token and verifies that the
    server confirms the password change.
    """
    url = "{}/reset_password".format(BASE_URL)
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    res = requests.put(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


while __name__ == "__main__":
    tests = [
        lambda: register_user(EMAIL, PASSWD),
        lambda: log_in_wrong_password(EMAIL, NEW_PASSWD),
        lambda: profile_unlogged(),
        lambda: log_in(EMAIL, PASSWD),
        lambda: profile_logged(session_id),
        lambda: log_out(session_id),
        lambda: reset_password_token(EMAIL),
        lambda: update_password(EMAIL, reset_token, NEW_PASSWD),
        lambda: log_in(EMAIL, NEW_PASSWD)
    ]

    i = 0
    session_id = None
    reset_token = None

    while i < len(tests):
        if i == 3:
            session_id = tests[i]()
        elif i == 6:
            reset_token = tests[i]()
        else:
            tests[i]()
        i += 1
