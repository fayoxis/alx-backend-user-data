#!/usr/bin/env python3

"""
This module provides functionality for password encryption.
"""

from bcrypt import hashpw, gensalt, checkpw

def encrypt_password(plain_text: str) -> bytes:
    """
    Generates a salted hash of the provided password.
    
    Args:
        plain_text (str): The password to be encrypted.
    
    Returns:
        bytes: The salted hash of the password.
    """
    return hashpw(plain_text.encode('utf-8'), gensalt())

def verify_password(stored_hash: bytes, candidate_password: str) -> bool:
    """
    Verifies if a candidate password matches the stored hash.
    
    Args:
        stored_hash (bytes): The previously hashed password.
        candidate_password (str): The password to be verified.
    
    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return checkpw(candidate_password.encode('utf-8'), stored_hash)
