#!/usr/bin/env python3
"""This is the Base module."""

import json
import uuid
from os import path
from datetime import datetime
from typing import TypeVar, List, Iterable

# Format for datetime
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
# Data storage
DATA = {}


class Base:
    """The Base class for all other classes."""

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a Base instance.
        *args: List of arguments.
        **kwargs: Dictionary of keyword arguments.
        """
        # Get the class name as a string
        s_class = str(self.__class__.__name__)
        # If the class doesn't exist in DATA, create a new dictionary for it
        if DATA.get(s_class) is None:
            DATA[s_class] = {}

        # Initialize the id
        self.id = kwargs.get('id', str(uuid.uuid4()))

        # Initialize the created_at attribute
        if kwargs.get('created_at') is not None:
            self.created_at = datetime.strptime(kwargs.get('created_at'),
                                                TIMESTAMP_FORMAT)
        else:
            self.created_at = datetime.utcnow()

        # Initialize the updated_at attribute
        if kwargs.get('updated_at') is not None:
            self.updated_at = datetime.strptime(kwargs.get('updated_at'),
                                                TIMESTAMP_FORMAT)
        else:
            self.updated_at = datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """Check if two instances are equal.
        other: The other instance to compare.
        Returns:True if the instances are equal, False otherwise.
        """
        # Check if the types are different
        if type(self) != type(other):
            return False
        # Check if the instance is not a Base instance
        if not isinstance(self, Base):
            return False
        # Compare the ids
        return (self.id == other.id)

    def to_json(self, for_serialization: bool = False) -> dict:
        """Convert the object to a JSON dictionary.Args:
        for_serialization: If True, remove private attributes.
        Returns:A dictionary representing the object.
        """
        result = {}
        for key, value in self.__dict__.items():
            # Skip private attributes if for_serialization is False
            if not for_serialization and key[0] == '_':
                continue
            # Convert datetime objects to strings
            if type(value) is datetime:
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                result[key] = value
        return result

    @classmethod
    def load_from_file(cls):
        """Load all objects from file."""
        # Get the class name as a string
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        DATA[s_class] = {}
        # Check if the file exists
        if not path.exists(file_path):
            return

        # Load objects from the file
        with open(file_path, 'r') as f:
            objs_json = json.load(f)
            for obj_id, obj_json in objs_json.items():
                DATA[s_class][obj_id] = cls(**obj_json)

    @classmethod
    def save_to_file(cls):
        """Save all objects to file."""
        # Get the class name as a string
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        objs_json = {}
        # Convert objects to JSON
        for obj_id, obj in DATA[s_class].items():
            objs_json[obj_id] = obj.to_json(True)

        # Save objects to file
        with open(file_path, 'w') as f:
            json.dump(objs_json, f)

    def save(self):
        """Save the current object."""
        # Get the class name as a string
        s_class = self.__class__.__name__
        # Update the updated_at attribute
        self.updated_at = datetime.utcnow()
        # Save the object
        DATA[s_class][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """Remove the current object."""
        # Get the class name as a string
        s_class = self.__class__.__name__
        # Check if the object exists in DATA
        if DATA[s_class].get(self.id) is not None:
            del DATA[s_class][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """
        Count all objects.
        Returns:
            The number of objects.
        """
        # Get the class name as a string
        s_class = cls.__name__
        # Count the number of objects
        return len(DATA[s_class].keys())

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """
        Return all objects.
        Returns:
            An iterable containing all objects.
        """
        return cls.search()

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """ Return one object by ID.Args:
        id: The ID of the object.Returns:The object
        with the given ID, or None if not found.
        """
        # Get the class name as a string
        s_class = cls.__name__
        return DATA[s_class].get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """Search for objects with matching attributes.Args:
        attributes: A dictionary of attribute-value pairs.
        Returns:A list of objects that match the given attributes.
        """
        # Get the class name as a string
        s_class = cls.__name__

        def _search(obj):
            """Helper function to check if an object matches
            the given attributes. obj: The object to check.
            Returns:True if the object matches the given 
            attributes, False otherwise.
            """
            # If no attributes are given, return True
            if len(attributes) == 0:
                return True
            # Check if the object has the given attributes
            for k, v in attributes.items():
                if (getattr(obj, k) != v):
                    return False
            return True

        # Filter objects based on the given attributes
        return list(filter(_search, DATA[s_class].values()))
