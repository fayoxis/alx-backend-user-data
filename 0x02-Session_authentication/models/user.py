"""User module for authentication and user management.
"""
import hashlib
from models.base import Base


class User(Base):
    """User class for authentication and user management.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a User instance with email, password,
        first name, and last name.
        """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @property
    def password(self) -> str:
        """Get the hashed password."""
        return self._password

    @password.setter
    def password(self, pwd: str):
        """Set a new password by hashing it with SHA256.
        WARNING: Use a better password hashing algorithm like argon2
        or bcrypt in real-world projects.
        """
        if pwd is None or type(pwd) is not str:
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: str) -> bool:
        """Check if the provided password matches
        the stored hashed password.
        """
        if pwd is None or type(pwd) is not str:
            return False
        if self.password is None:
            return False
        pwd_e = pwd.encode()
        return hashlib.sha256(pwd_e).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """Generate a display name for the user
        based on available information.
        """
        if self.email is None and self.first_name is None \
                and self.last_name is None:
            return ""
        if self.first_name is None and self.last_name is None:
            return "{}".format(self.email)
        if self.last_name is None:
            return "{}".format(self.first_name)
        if self.first_name is None:
            return "{}".format(self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)
