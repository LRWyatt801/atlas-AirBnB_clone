#!/usr/bin/python3
"""Module contains BaseModel
BaseModel: defines all common attributes/methods
            for other classes
"""


from datetime import datetime
import uuid
import models


class BaseModel:
    """Defines all common attributes and methods
    for other classes
    """
    def __init__(self, *args, **kwargs) -> None:
        """Initialize instance with random UUID
        and timestamps for created_at and updated_at
        """
        if kwargs:  # Create instance from dict/json
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    setattr(self, key, datetime.fromisoformat(value))
                elif key == '__class__':
                    pass
                else:
                    setattr(self, key, value)

        else:  # Create brand new instance
            new_id = uuid.uuid4()  # Asign random UUID
            self.id = str(new_id)
            self.created_at = datetime.now()  # Created timestamp
            self.updated_at = datetime.now()  # Update timestamp
            models.storage.new(self)

    def __str__(self) -> str:
        """Change string representation of class instance to:
        [<class name>] (<self.id>) <self.__dict__>

        Returns:
            str: String representation of class instance
        """
        return ("[{}] ({}) {}"
                .format(
                    self.__class__.__name__,
                    self.id,
                    self.__dict__
                ))

    def save(self) -> None:
        """Updates timestamp for updated_at
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self) -> dict:
        """Returns a dictionary containing all keys:values
        of __dict__ of the instance

        Returns:
            dict: Dictionary representation of instance
        """
        # Copy instance dict to manipulate
        # w/o changing orignal
        dict_copy = self.__dict__.copy()

        # Convert timestamps to strings
        dict_copy['created_at'] = self.created_at.isoformat()
        dict_copy['updated_at'] = self.updated_at.isoformat()

        # Add the __class__ key
        dict_copy['__class__'] = self.__class__.__name__

        return dict_copy
