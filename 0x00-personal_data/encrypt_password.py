#!/usr/bin/env python3
"""This module provides functionality 4 password encryption.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Generates a salted hash of the provided password.
    plain_text (str): The password to be encrypted.
    bytes: The salted hash of the password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Verifies if a candidate password matches the stored hash.
    stored_hash (bytes): The previously hashed password.
    candidate_password (str): The password to be verified.
    bool: True if the password matches the hash, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
