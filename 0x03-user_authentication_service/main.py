#!/usr/bin/env python3
"""A simple end-to-end integration
test for the `app.py` application.
"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"

def register_user(email: str, password: str) -> None:
    """Register a new user with the
    provided email and password.
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
    """Attempt to log in with the wrong password."""
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 401

def log_in(email: str, password: str) -> str:
    """Log in with the provided email and password."""
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
    """Attempt to access the
    user profile while not logged in.
    """
    url = "{}/profile".format(BASE_URL)
    res = requests.get(url)
    assert res.status_code == 403

def profile_logged(session_id: str) -> None:
    """Access the user profile while logged in.
    """
    url = "{}/profile".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.get(url, cookies=req_cookies)
    assert res.status_code == 200
    assert "email" in res.json()

def log_out(session_id: str) -> None:
    """Log out of the current session.
    """
    url = "{}/sessions".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.delete(url, cookies=req_cookies)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}

def reset_password_token(email: str) -> str:
    """Request a password reset token for the provided email.
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
    """Update the user's password using the reset token.
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

if __name__ == "__main__":
    i = 0
    while i < 9:
        if i == 0:
            register_user(EMAIL, PASSWD)
        elif i == 1:
            log_in_wrong_password(EMAIL, NEW_PASSWD)
        elif i == 2:
            profile_unlogged()
        elif i == 3:
            session_id = log_in(EMAIL, PASSWD)
        elif i == 4:
            profile_logged(session_id)
        elif i == 5:
            log_out(session_id)
        elif i == 6:
            reset_token = reset_password_token(EMAIL)
        elif i == 7:
            update_password(EMAIL, reset_token, NEW_PASSWD)
        elif i == 8:
            log_in(EMAIL, NEW_PASSWD)
        i += 1
