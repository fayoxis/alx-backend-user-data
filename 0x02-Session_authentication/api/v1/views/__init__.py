#!/usr/bin/env python3
"""
This module sets up the Blueprint for the API views
and imports the necessary view modules and models.
"""

from flask import Blueprint
import os

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import view modules
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *

# Load user data from file
from models.user import User
User.load_from_file()
