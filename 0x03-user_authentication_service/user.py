#!/usr/bin/env python3
"""This module defines the User model for the application."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for declarative class definitions
Base = declarative_base()

class User(Base):
    """Represents a user record in the database.

    Attributes:
        id (int): Primary key for the user record.
        email (str): User's email address (max length: 250 characters).
        hashed_password (str): Hashed value of the user's password
            (max length: 250 characters).
        session_id (str, optional): User's current session ID
            (max length: 250 characters).
        reset_token (str, optional): Token for resetting the user's password
            (max length: 250 characters).
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
